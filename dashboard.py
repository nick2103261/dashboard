import streamlit as st
import pandas as pd
from datetime import date
import os

ARQUIVO_DADOS = "dados_financeiros.csv"

st.set_page_config(page_title="💸 Dashboard Financeiro", page_icon="💰", layout="wide")

st.title("💸 Dashboard Financeiro Pessoal")
st.caption("Gerencie seus ganhos e gastos. Acesse do PC ou celular!")

# ===== FORMULÁRIO DE MOVIMENTAÇÃO =====
with st.form("formulario"):
    st.subheader("Adicionar nova movimentação")

    data = st.date_input("Data", value=date.today())
    tipo = st.radio("Tipo", ["Ganho", "Gasto"], horizontal=True)
    categoria = st.text_input("Categoria", placeholder="Ex: Mercado, Salário, Transporte")
    descricao = st.text_input("Descrição (opcional)")
    valor = st.number_input("Valor", min_value=0.01, step=0.01)

    enviado = st.form_submit_button("Salvar")

    if enviado:
        nova_linha = pd.DataFrame([[data, tipo, categoria, descricao, valor]],
                                  columns=["Data", "Tipo", "Categoria", "Descrição", "Valor"])

        if os.path.exists(ARQUIVO_DADOS):
            df_existente = pd.read_csv(ARQUIVO_DADOS)
            df = pd.concat([df_existente, nova_linha], ignore_index=True)
        else:
            df = nova_linha

        df.to_csv(ARQUIVO_DADOS, index=False)
        st.success("Movimentação salva com sucesso! ✅")

# ===== CARREGAMENTO DOS DADOS =====
if os.path.exists(ARQUIVO_DADOS):
    df = pd.read_csv(ARQUIVO_DADOS, parse_dates=["Data"])
    df = df.sort_values("Data")

    st.subheader("📋 Histórico de Movimentações")
    st.dataframe(df, use_container_width=True, hide_index=True)

    ganhos = df[df["Tipo"] == "Ganho"]["Valor"].sum()
    gastos = df[df["Tipo"] == "Gasto"]["Valor"].sum()
    saldo = ganhos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ganhos", f"R$ {ganhos:.2f}")
    col2.metric("💸 Gastos", f"R$ {gastos:.2f}")
    col3.metric("📊 Saldo", f"R$ {saldo:.2f}")

    # ===== GRÁFICOS =====
    st.subheader("📈 Evolução financeira")
    grafico_evolucao = df.groupby("Data")["Valor"].sum()
    st.line_chart(grafico_evolucao)

    st.subheader("📊 Gastos por categoria")
    categorias = df[df["Tipo"] == "Gasto"].groupby("Categoria")["Valor"].sum()
    if not categorias.empty:
        st.bar_chart(categorias)
    else:
        st.info("Nenhum gasto registrado ainda.")

else:
    st.warning("Nenhuma movimentação encontrada. Comece adicionando dados acima.")
