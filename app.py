import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Whey", page_icon="💪", layout="wide")

st.title("💪 Calculadora de Custo-Benefício de Whey Protein")
st.markdown("Compare seus suplementos e descubra **qual realmente vale mais a pena!**")

# Inicializa lista de produtos na sessão
if "produtos" not in st.session_state:
    st.session_state.produtos = []

# Formulário para adicionar produto
with st.form("add_produto"):
    st.subheader("➕ Adicionar Produto")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do produto (ex.: Whey FTW Chocolate)")
        peso_total = st.number_input("Peso total da embalagem (g)", min_value=100, step=100)
        dose = st.number_input("Gramas por dose (ex.: 30)", min_value=1, step=1)
    with col2:
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

# Se houver produtos adicionados, mostra cards + tabela comparativa
if st.session_state.produtos:
    st.subheader("📊 Comparação dos Produtos")

    df = pd.DataFrame(st.session_state.produtos)

    # Cálculos adicionais
    df["Nº de doses"] = (df["Peso total (g)"] / df["Dose (g)"]).astype(int)
    df["Proteína total (g)"] = df["Nº de doses"] * df["Proteína/dose (g)"]
    df["R$/g Whey"] = (df["Preço (R$)"] / df["Peso total (g)"]).round(2)
    df["R$/g Proteína"] = (df["Preço (R$)"] / df["Proteína total (g)"]).round(2)
    df["R$/dose"] = (df["Preço (R$)"] / df["Nº de doses"]).round(2)

    # Exibir cards individuais
    st.markdown("### 🏷️ Produtos adicionados")
    for _, row in df.iterrows():
        st.markdown(
            f"""
            <div style="background:#f0f2f6; padding:15px; border-radius:12px; margin-bottom:10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.1);">
                <h4>{row['Produto']}</h4>
                <ul>
                    <li><b>Peso total:</b> {row['Peso total (g)']} g</li>
                    <li><b>Dose:</b> {row['Dose (g)']} g</li>
                    <li><b>Proteína por dose:</b> {row['Proteína/dose (g)']} g</li>
                    <li><b>Preço:</b> R$ {row['Preço (R$)']:.2f}</li>
                    <li><b>Nº de doses:</b> {row['Nº de doses']}</li>
                    <li><b>Proteína total:</b> {row['Proteína total (g)']} g</li>
                    <li><b>Custo por dose:</b> R$ {row['R$/dose']:.2f}</li>
                    <li><b>Custo por g de whey:</b> R$ {row['R$/g Whey']:.2f}</li>
                    <li><b>Custo por g de proteína:</b> R$ {row['R$/g Proteína']:.2f}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 📋 Tabela comparativa")
    st.dataframe(df, use_container_width=True)

    # Botão para resetar lista
    if st.button("🔄 Limpar produtos"):
        st.session_state.produtos = []
        st.rerun()
else:
    st.info("Nenhum produto adicionado ainda.")
