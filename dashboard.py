import streamlit as st
import pandas as pd
import datetime

# Aplicando estilo responsivo para versão mobile e desktop
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, label {
            color: white !important;
        }
        .stDataFrame, .dataframe {
            background-color: #1E1E1E !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
        }
        .stSelectbox, .stTextInput, .stNumberInput, .stDataFrame {
            background-color: #121212 !important;
            color: white !important;
            border-radius: 8px;
            padding: 8px;
        }
        .stSelectbox label {
            color: white !important;
        }
        .stSelectbox select {
            color: black !important;
        }
        .stSelectbox div[role="listbox"] {
            background-color: #1E1E1E !important;
            color: black !important;
        }
        .stHeader, .stTitle {
            color: white !important;
        }
        .stButton > button {
            background-color: #003F74 !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
        }
        .stSuccess {
            background-color: #28a745 !important;
            color: white !important;
        }
        .stTable {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
            font-size: 16px;
            text-align: center;
        }
        .stTable th, .stTable td {
            border: 1px solid #ddd;
            padding: 12px;
            color: white !important;
        }
        .stTable th {
            background-color: #003F74;
            color: white;
            font-weight: bold;
        }
        .stTable tr:nth-child(even) {
            background-color: #2a2a2a;
        }
        .stTable tr:nth-child(odd) {
            background-color: #1E1E1E;
        }
        @media (max-width: 768px) {
            .stColumns {
                flex-direction: column !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Função para carregar ou criar o arquivo de torneios
def load_data():
    try:
        df = pd.read_csv("torneios.csv")
        return df if not df.empty else pd.DataFrame(columns=["Dia", "Horário", "Valor", "Entrada"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Dia", "Horário", "Valor", "Entrada"])

def save_data(df):
    df.to_csv("torneios.csv", index=False)

# Exibir logo centralizada
st.image("logo.png", width=125)


# Carregar os dados
st.title("🏆 Dashboard de Torneios - Liga Brasil 🏆")

df = load_data()

# Adicionar novo torneio
st.header("Adicionar Novo Torneio")
dias_da_semana = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"]
dia = st.selectbox("Dia da Semana", dias_da_semana)

horarios_disponiveis = ["11:00", "16:00", "21:00"]
horario = st.selectbox("Horário", horarios_disponiveis)

valor = st.number_input("Valor do Torneio (R$)", min_value=0.0, format="%.2f")
entrada = st.number_input("Valor da Entrada", min_value=0, step=1)

if st.button("Adicionar Torneio"):
    novo_torneio = pd.DataFrame([[dia, horario, valor, entrada]], columns=df.columns)
    df = pd.concat([df, novo_torneio], ignore_index=True)
    save_data(df)
    st.success("✅ Torneio adicionado com sucesso!")

# Exibir lista de torneios separados por dia da semana em colunas responsivas
st.header("Torneios Cadastrados")
if not df.empty:
    df_display = df[['Horário', 'Valor', 'Entrada']].copy()
    df_display["Valor"] = df_display["Valor"].apply(lambda x: f"R$ {float(x):,.2f}" if isinstance(x, (int, float)) else x)
    df_display["Entrada"] = df_display["Entrada"].apply(lambda x: f"R$ {float(x):,.2f}" if isinstance(x, (int, float)) else x)
    
    col1, col2 = st.columns(2) if st.get_option("browser.gatherUsageStats") else (st.container(), st.container())
    for i, dia in enumerate(dias_da_semana):
        torneios_do_dia = df_display[df["Dia"] == dia].reset_index(drop=True)
        if not torneios_do_dia.empty:
            if i % 2 == 0:
                with col1:
                    st.subheader(f"🗓️ {dia}")
                    st.dataframe(torneios_do_dia, hide_index=True)
            else:
                with col2:
                    st.subheader(f"🗓️ {dia}")
                    st.dataframe(torneios_do_dia, hide_index=True)

# Opção para excluir torneios
st.header("Excluir Torneio")
if not df.empty:
    opcoes = ["Excluir Todos"] + df.apply(lambda row: f"{row['Dia']} - {row['Horário']} - R$ {row['Valor']} - Entrada R$ {row['Entrada']}", axis=1).tolist()
    torneio_selecionado = st.selectbox("Selecione um torneio para excluir", opcoes)
    
    if st.button("Excluir Torneio"):
        if torneio_selecionado == "Excluir Todos":
            df = pd.DataFrame(columns=["Dia", "Horário", "Valor", "Entrada"])
            st.success("✅ Todos os torneios foram excluídos!")
        else:
            df = df[df.apply(lambda row: f"{row['Dia']} - {row['Horário']} - R$ {row['Valor']} - Entrada R$ {row['Entrada']}" != torneio_selecionado, axis=1)]
            st.success("✅ Torneio excluído com sucesso!")
        save_data(df)

st.write("⚡ Desenvolvido para a gestão dos torneios da Liga Brasil ⚡")
