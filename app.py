import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Whey", page_icon="💪", layout="centered")

st.title("💪 Calculadora de Custo-Benefício de Whey Protein")
st.write("Compare seus suplementos e descubra qual realmente vale mais a pena!")

# Inicializa lista de produtos na sessão
if "produtos" not in st.session_state:
    st.session_state.produtos = []

# Formulário para adicionar produto
with st.form("add_produto"):
    st.subheader("➕ Adicionar Produto")
    nome = st.text_input("Nome do produto (ex.: Whey FTW Chocolate)")
    peso_total = st.number_input("Peso total da embalagem (g)", min_value=100, step=100)
    dose = st.number_input("Gramas por dose (ex.: 30)", min_value=1, step=1)
    proteina_dose = st.number_input("Proteína por dose (g)", min_value=1, step=1)
    preco = st.number_input("Preço pago (R$)", min_value=0.0, step=1.0, format="%.2f")

    adicionar = st.form_submit_button("Adicionar produto")

    if adicionar and nome:
        st.session_state.produtos.append({
            "Produto": nome,
            "Peso total (g)": peso_total,
            "Dose (g)": dose,
            "Proteína/dose (g)": proteina_dose,
            "Preço (R$)": preco
        })
        st.success(f"{nome} adicionado com sucesso!")

# Se houver produtos adicionados, mostra tabela comparativa
if st.session_state.produtos:
    st.subheader("📊 Comparação dos Produtos")

    df = pd.DataFrame(st.session_state.produtos)

    # Cálculos adicionais
    df["Nº de doses"] = (df["Peso total (g)"] / df["Dose (g)"]).astype(int)
    df["Proteína total (g)"] = df["Nº de doses"] * df["Proteína/dose (g)"]
    df["R$/g Whey"] = (df["Preço (R$)"] / df["Peso total (g)"]).round(2)
    df["R$/g Proteína"] = (df["Preço (R$)"] / df["Proteína total (g)"]).round(2)
    df["R$/dose"] = (df["Preço (R$)"] / df["Nº de doses"]).round(2)

    st.dataframe(df, use_container_width=True)

    # Botão para resetar lista
    if st.button("🔄 Limpar produtos"):
        st.session_state.produtos = []
        st.rerun()
else:
    st.info("Nenhum produto adicionado ainda.")
