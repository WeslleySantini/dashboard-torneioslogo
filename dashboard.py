import streamlit as st
import pandas as pd
import uuid

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
        # Se a coluna 'ID' não existir (para compatibilidade), cria-a
        if "ID" not in df.columns:
            df["ID"] = [str(uuid.uuid4()) for _ in range(len(df))]
            save_data(df)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["ID", "Dia", "Horário", "Valor", "Entrada"])

def save_data(df):
    df.to_csv("torneios.csv", index=False)

# Exibir logo centralizada
st.image("logo.png", width=250)

# Título do dashboard
st.title("Dashboard de Torneios - Liga Brasil")

# Carregar os dados
df = load_data()

# -------------------------------
# Adicionar novo torneio
# -------------------------------
st.header("Adicionar Novo Torneio")
dias_da_semana = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"]
dia = st.selectbox("Dia da Semana", dias_da_semana)

horarios_disponiveis = ["11:00", "16:00", "21:00"]
horario = st.selectbox("Horário", horarios_disponiveis)

valor = st.number_input("Valor do Torneio (R$)", min_value=0.0, format="%.2f")
entrada = st.number_input("Valor da Entrada", min_value=0, step=1)

if st.button("Adicionar Torneio"):
    if valor < 0 or entrada < 0:
        st.error("Valores inválidos! Por favor, insira números não negativos.")
    else:
        # Gerar um ID único para o torneio
        new_id = str(uuid.uuid4())
        novo_torneio = pd.DataFrame([[new_id, dia, horario, valor, entrada]], 
                                    columns=["ID", "Dia", "Horário", "Valor", "Entrada"])
        df = pd.concat([df, novo_torneio], ignore_index=True)
        save_data(df)
        st.success("✅ Torneio adicionado com sucesso!")
        st.experimental_rerun()  # Atualiza a página para refletir a alteração

# -------------------------------
# Exibir lista de torneios cadastrados
# -------------------------------
st.header("Torneios Cadastrados")
if not df.empty:
    col1, col2 = st.columns(2)
    for i, dia_semana in enumerate(dias_da_semana):
        torneios_do_dia = df[df["Dia"] == dia_semana]
        if not torneios_do_dia.empty:
            # Exibir sem a coluna 'ID' para uma melhor visualização
            if i % 2 == 0:
                with col1:
                    st.subheader(f"🗓️ {dia_semana}")
                    st.dataframe(torneios_do_dia.drop(columns=["ID"]))
            else:
                with col2:
                    st.subheader(f"🗓️ {dia_semana}")
                    st.dataframe(torneios_do_dia.drop(columns=["ID"]))

# -------------------------------
# Excluir torneio
# -------------------------------
st.header("Excluir Torneio")
if not df.empty:
    # Criar mapeamento: ID -> Descrição para exibição
    tournament_ids = df['ID'].tolist()
    display_mapping = {row['ID']: f"{row['Dia']} - {row['Horário']} - R${row['Valor']} - Entrada {row['Entrada']}" 
                       for _, row in df.iterrows()}
    selected_id = st.selectbox("Selecione um torneio para excluir", 
                               tournament_ids, 
                               format_func=lambda x: display_mapping[x])
    if st.button("Excluir Torneio"):
        df = df[df['ID'] != selected_id]
        save_data(df)
        st.success("✅ Torneio excluído com sucesso!")
        st.experimental_rerun()

# -------------------------------
# Editar torneio
# -------------------------------
st.header("Editar Torneio")
if not df.empty:
    tournament_ids_edit = df['ID'].tolist()
    display_mapping_edit = {row['ID']: f"{row['Dia']} - {row['Horário']} - R${row['Valor']} - Entrada {row['Entrada']}" 
                            for _, row in df.iterrows()}
    selected_id_edit = st.selectbox("Selecione um torneio para editar", 
                                    tournament_ids_edit, 
                                    format_func=lambda x: display_mapping_edit[x])
    # Obter os dados do torneio selecionado
    tournament_to_edit = df[df['ID'] == selected_id_edit].iloc[0]
    with st.form(key='edit_tournament_form'):
        dia_edit = st.selectbox("Dia da Semana", dias_da_semana, index=dias_da_semana.index(tournament_to_edit["Dia"]))
        horario_edit = st.selectbox("Horário", horarios_disponiveis, index=horarios_disponiveis.index(tournament_to_edit["Horário"]))
        valor_edit = st.number_input("Valor do Torneio (R$)", min_value=0.0, 
                                     value=float(tournament_to_edit["Valor"]), format="%.2f")
        entrada_edit = st.number_input("Valor da Entrada", min_value=0, 
                                       value=int(tournament_to_edit["Entrada"]), step=1)
        submit_edit = st.form_submit_button("Salvar Alterações")
    if submit_edit:
        df.loc[df['ID'] == selected_id_edit, "Dia"] = dia_edit
        df.loc[df['ID'] == selected_id_edit, "Horário"] = horario_edit
        df.loc[df['ID'] == selected_id_edit, "Valor"] = valor_edit
        df.loc[df['ID'] == selected_id_edit, "Entrada"] = entrada_edit
        save_data(df)
        st.success("✅ Torneio atualizado com sucesso!")
        st.experimental_rerun()

st.write("Desenvolvido para a gestão dos torneios da Liga Brasil")
