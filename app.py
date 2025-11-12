import streamlit as st
import pandas as pd
import os

# Caminho base das imagens no GitHub (Render vai usar essa URL)
BASE_URL = "https://raw.githubusercontent.com/mostruario/catalogo_pronta_entrega/main/STATIC/IMAGENS/"

# Carrega planilha
file_path = "ESTOQUE PRONTA ENTREGA CLAMI.xlsx"
df = pd.read_excel(file_path)

# Normaliza nomes das colunas (tira espaços, maiúsculas etc.)
df.columns = df.columns.str.strip().str.upper()

# Ajusta nomes esperados
col_map = {
    "MARCA": "MARCA",
    "COMP.": "COMP.",
    "ALT.": "ALT.",
    "LARG.": "LARG.",
    "DESCRIÇÃO": "DESCRIÇÃO",
    "IMAGEM": "IMAGEM"
}
df = df.rename(columns={c: col_map[c] for c in df.columns if c in col_map})

# Sidebar - Filtro
st.sidebar.title("Filtros")
marcas = df["MARCA"].dropna().unique()
marca_select = st.sidebar.multiselect("Selecione a marca", marcas)

# Filtra por marca
if marca_select:
    df = df[df["MARCA"].isin(marca_select)]

# Título
st.title("🛋️ Catálogo de Produtos - Pronta Entrega")

# Loop para exibir os produtos
for _, row in df.iterrows():
    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            imagem = str(row.get("IMAGEM", "")).strip()
            if imagem and imagem != "nan":
                image_url = BASE_URL + imagem.replace(" ", "%20")
                st.image(image_url, use_container_width=True)
            else:
                st.image(BASE_URL + "SEM%20IMAGEM.jpg", use_container_width=True)

        with col2:
            st.markdown(f"### {row.get('DESCRIÇÃO', '')}")
            st.markdown(f"**Marca:** {row.get('MARCA', '')}")
            st.markdown(
                f"<small><b>Comp.:</b> {row.get('COMP.', '')} | "
                f"<b>Alt.:</b> {row.get('ALT.', '')} | "
                f"<b>Larg.:</b> {row.get('LARG.', '')}</small>",
                unsafe_allow_html=True
            )

st.markdown("---")
st.markdown("<center><small>Catálogo automático - CLAMI</small></center>", unsafe_allow_html=True)
