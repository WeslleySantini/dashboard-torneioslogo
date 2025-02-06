import streamlit as st
import pandas as pd
import datetime

# Função para carregar ou criar o arquivo de torneios
def load_data():
    try:
        return pd.read_csv("torneios.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Dia", "Horário", "Valor", "Entrada"])

def save_data(df):
    df.to_csv("torneios.csv", index=False)

# Exibir logo centralizada
st.image("logo.png", width=200)

# Carregar os dados
st.title("Dashboard de Torneios - Liga Brasil")

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
    st.success("Torneio adicionado com sucesso!")

# Exibir lista de torneios separados por dia da semana
st.header("Torneios Cadastrados")
if not df.empty:
    for dia in dias_da_semana:
        torneios_do_dia = df[df["Dia"] == dia]
        if not torneios_do_dia.empty:
            st.subheader(dia)
            st.dataframe(torneios_do_dia)

# Opção para excluir torneios
st.header("Excluir Torneio")
if not df.empty:
    torneio_selecionado = st.selectbox("Selecione um torneio para excluir", df.apply(lambda row: f"{row['Dia']} - {row['Horário']} - R${row['Valor']} - Entrada {row['Entrada']}", axis=1))
    if st.button("Excluir Torneio"):
        df = df[df.apply(lambda row: f"{row['Dia']} - {row['Horário']} - R${row['Valor']} - Entrada {row['Entrada']}" != torneio_selecionado, axis=1)]
        save_data(df)
        st.success("Torneio excluído com sucesso!")

st.write("Desenvolvido para gestão dos torneios diários da Liga Brasil.")
