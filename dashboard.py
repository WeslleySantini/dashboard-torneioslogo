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
        p, div, span, button {
            color: white !important;
        }
        .stDataFrame, .dataframe {
            background-color: #1E1E1E !important;
            color: white !important;
        }
        .stSelectbox, .stButton, .stTextInput, .stNumberInput, .stDataFrame {
            background-color: #121212 !important;
            color: black !important;
            border-radius: 8px;
            padding: 8px;
        }
        .stSelectbox * {
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
            background-color: #1E1E1E !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
        }
        .stSuccess {
            background-color: #28a745 !important;
            color: white !important;
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
        return pd.read_csv("torneios.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Dia", "Horário", "Valor", "Entrada"])

def save_data(df):
    df.to_csv("torneios.csv", index=False)

# Exibir logo centralizada
st.image("logo.png", width=250)

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
    col1, col2 = st.columns(2) if st.get_option("browser.gatherUsageStats") else (st.container(), st.container())
    for i, dia in enumerate(dias_da_semana):
        torneios_do_dia = df[df["Dia"] == dia]
        if not torneios_do_dia.empty:
            if i % 2 == 0:
                with col1:
                    st.subheader(f"🗓️ {dia}")
                    st.dataframe(torneios_do_dia)
            else:
                with col2:
                    st.subheader(f"🗓️ {dia}")
                    st.dataframe(torneios_do_dia)

# Opção para excluir torneios
st.header("Excluir Torneio")
if not df.empty:
    torneio_selecionado = st.selectbox("Selecione um torneio para excluir", df.apply(lambda row: f"{row['Dia']} - {row['Horário']} - R${row['Valor']} - Entrada {row['Entrada']}", axis=1))
    if st.button("Excluir Torneio"):
        df = df[df.apply(lambda row: f"{row['Dia']} - {row['Horário']} - R${row['Valor']} - Entrada {row['Entrada']}" != torneio_selecionado, axis=1)]
        save_data(df)
        st.success("✅ Torneio excluído com sucesso!")

st.write("⚡ Desenvolvido para a gestão dos torneios da Liga Brasil ⚡")
