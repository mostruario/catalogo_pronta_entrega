import streamlit as st
import pandas as pd
import os

# ---------- CONFIGURAÇÃO ----------
st.set_page_config(page_title="Catálogo - Pronta Entrega", layout="wide")

# Caminho base das imagens no GitHub (Render usa essa URL)
BASE_URL = "https://raw.githubusercontent.com/mostruario/catalogo_pronta_entrega/main/STATIC/IMAGENS/"

# ---------- DEBUG (mostrar URLs das imagens no app) ----------
DEBUG = True  # deixe True até confirmarmos que as imagens aparecem

# ---------- CARREGAR PLANILHA ----------
file_path = "ESTOQUE PRONTA ENTREGA CLAMI.xlsx"
if not os.path.exists(file_path):
    st.error("❌ Arquivo da planilha não foi encontrado no Render.")
    st.stop()

df = pd.read_excel(file_path)
df.columns = df.columns.str.strip().str.upper()

# Corrige nomes padrão
col_map = {
    "MARCA": "MARCA",
    "COMP.": "COMP.",
    "ALT.": "ALT.",
    "LARG.": "LARG.",
    "DESCRIÇÃO": "DESCRIÇÃO",
    "IMAGEM": "IMAGEM"
}
df = df.rename(columns={c: col_map[c] for c in df.columns if c in col_map})

# ---------- FILTROS ----------
st.sidebar.title("Filtros")
marcas = df["MARCA"].dropna().unique()
marca_select = st.sidebar.multiselect("Selecione a marca", marcas)

if marca_select:
    df = df[df["MARCA"].isin(marca_select)]

# ---------- TÍTULO ----------
st.title("🛋️ Catálogo de Produtos - Pronta Entrega")

# ---------- EXIBIÇÃO DOS PRODUTOS ----------
for _, row in df.iterrows():
    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            imagem = str(row.get("IMAGEM", "")).strip()
            if imagem and imagem != "nan":
                image_url = BASE_URL + imagem.replace(" ", "%20")
            else:
                image_url = BASE_URL + "SEM%20IMAGEM.jpg"

            # Mostra a imagem
            st.image(image_url, use_container_width=True)

            # Mostra a URL da imagem para debug
            if DEBUG:
                st.caption(f"🔍 URL da imagem: `{image_url}`")

        with col2:
            st.markdown(f"### {row.get('DESCRIÇÃO', '')}")
            st.markdown(f"**Marca:** {row.get('MARCA', '')}")
            st.markdown(
                f"<small><b>Comp.:</b> {row.get('COMP.', '')} | "
                f"<b>Alt.:</b> {row.get('ALT.', '')} | "
                f"<b>Larg.:</b> {row.get('LARG.', '')}</small>",
                unsafe_allow_html=True
            )

# ---------- RODAPÉ ----------
st.markdown("---")
st.markdown("<center><small>Catálogo automático - CLAMI</small></center>", unsafe_allow_html=True)
