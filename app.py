import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Calculadora de Whey Protein", page_icon="💪", layout="wide")

# Estilo customizado (fundo escuro bonito)
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    h1, h2, h3, h4 {
        color: #00ffb3 !important;
    }
    .css-1d391kg p, .css-1d391kg span {
        color: #e6e6e6 !important;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #1a1d24 !important;
    }
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #111418 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💪 Calculadora de Custo-Benefício do Whey Protein")
st.markdown("Compare suplementos de forma **justa** usando 30g como dose de referência. 🥛💥")

# Lista de produtos
produtos = []

qtd = st.slider("Quantos produtos deseja comparar?", min_value=1, max_value=6, value=2)

cols = st.columns(qtd)

for i in range(qtd):
    with cols[i]:
        st.markdown(f"### 🥤 Produto {i+1}")
        nome = st.text_input(f"Nome do Produto {i+1}", f"Whey {i+1}", key=f"nome{i}")
        peso_total = st.number_input(f"Peso total (g)", min_value=1, value=900, key=f"peso{i}")
        dose = st.number_input(f"Dose declarada (g)", min_value=1, value=30, key=f"dose{i}")
        proteina_dose = st.number_input(f"Proteína por dose (g)", min_value=1, value=21, key=f"prot{i}")
        preco = st.number_input(f"Preço pago (R$)", min_value=0.0, value=100.0, step=1.0, key=f"preco{i}")

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

    df["R$/dose (30g)"] = df["Preço (R$)"] / df["Nº de doses (30g ref)"]
    df["R$/g proteína (30g ref)"] = df["R$/dose (30g)"] / df["Proteína ajustada (30g)"]

    st.markdown("## 📊 Resultados Comparativos")
    st.dataframe(
        df[[
            "Produto",
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

    # Gráfico comparativo
    st.markdown("## 📉 Visualização")
    fig = px.bar(
        df,
        x="Produto",
        y="R$/g proteína (30g ref)",
        text=df["R$/g proteína (30g ref)"].map("R$ {:.2f}".format),
        color="Produto",
        color_discrete_sequence=px.colors.sequential.Viridis,
        title="💸 Custo por grama de proteína (30g de whey)",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#fafafa"),
        title_font=dict(color="#00ffb3", size=20),
    )
    st.plotly_chart(fig, use_container_width=True)
