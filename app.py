import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Whey Protein", page_icon="💪", layout="centered")

# Estilo com fundo escuro
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stApp {
        background-color: #0e1117;
    }
    table {
        color: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💪 Calculadora de Custo-Benefício do Whey Protein")

st.markdown("Compare diferentes suplementos de forma justa usando **30g como dose de referência**.")

# Lista para armazenar produtos
produtos = []

# Número de produtos que o usuário quer comparar
qtd = st.number_input("Quantos produtos deseja comparar?", min_value=1, max_value=10, value=2, step=1)

for i in range(qtd):
    st.subheader(f"Produto {i+1}")
    nome = st.text_input(f"Nome do Produto {i+1}", f"Whey {i+1}")
    peso_total = st.number_input(f"Peso total (g) - Produto {i+1}", min_value=1, value=900)
    dose = st.number_input(f"Tamanho da dose declarada (g) - Produto {i+1}", min_value=1, value=30)
    proteina_dose = st.number_input(f"Proteína por dose declarada (g) - Produto {i+1}", min_value=1, value=21)
    preco = st.number_input(f"Preço pago (R$) - Produto {i+1}", min_value=0.0, value=100.0, step=1.0)

    produtos.append({
        "Produto": nome,
        "Peso total (g)": peso_total,
        "Dose declarada (g)": dose,
        "Proteína declarada (g)": proteina_dose,
        "Preço (R$)": preco,
    })

if produtos:
    df = pd.DataFrame(produtos)

    # Dose de referência
    dose_ref = 30  

    # Cálculos
    df["Nº de doses declaradas"] = (df["Peso total (g)"] / df["Dose declarada (g)"]).astype(int)
    df["Proteína ajustada (30g)"] = (df["Proteína declarada (g)"] / df["Dose declarada (g)"]) * dose_ref
    df["Nº de doses (30g ref)"] = (df["Peso total (g)"] / dose_ref).astype(int)

    # Custos baseados na dose de referência
    df["R$/dose (30g)"] = df["Preço (R$)"] / df["Nº de doses (30g ref)"]
    df["R$/g proteína (30g ref)"] = df["R$/dose (30g)"] / df["Proteína ajustada (30g)"]

    st.subheader("📊 Resultados Comparativos")
    st.dataframe(
        df[[
            "Produto",
            "Peso total (g)",
            "Nº de doses (30g ref)",
            "Proteína ajustada (30g)",
            "R$/dose (30g)",
            "R$/g proteína (30g ref)"
        ]].style.format({
            "Proteína ajustada (30g)": "{:.1f} g",
            "R$/dose (30g)": "R$ {:.2f}",
            "R$/g proteína (30g ref)": "R$ {:.2f}"
        })
    )
