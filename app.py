import streamlit as st
import pandas as pd
from PIL import Image
import os

# ============ CONFIGURAÇÕES ============
st.set_page_config(page_title="Catálogo - Pronta Entrega", layout="wide")

# Caminho base do projeto (compatível com Render e Windows)
BASE_DIR = os.path.dirname(__file__)

# Caminhos para pastas
STATIC_DIR = os.path.join(BASE_DIR, "STATIC", "IMAGENS")
EXCEL_PATH = os.path.join(BASE_DIR, "ESTOQUE PRONTA ENTREGA CLAMI.xlsx")

# ============ LOGO ============
try:
    logo_path = os.path.join(STATIC_DIR, "logo.png")
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("⚠️ Logo não encontrada.")

# ============ CARREGAR DADOS ============
try:
    df = pd.read_excel(EXCEL_PATH)
except FileNotFoundError:
    st.error("❌ Arquivo de catálogo não encontrado. Verifique se 'ESTOQUE PRONTA ENTREGA CLAMI.xlsx' está no mesmo diretório do app.py.")
    st.stop()

# ============ FUNÇÃO PARA IMAGENS ============
def carregar_imagem(nome_arquivo):
    caminho = os.path.join(STATIC_DIR, nome_arquivo)
    if os.path.exists(caminho):
        return Image.open(caminho)
    else:
        return Image.open(os.path.join(STATIC_DIR, "SEM IMAGEM.jpg"))

# ============ TÍTULO ============
st.title("📦 Catálogo - Pronta Entrega")
st.markdown("Explore os produtos disponíveis em nosso estoque!")

# ============ CAMPO DE PESQUISA ============
st.markdown("### 🔍 Pesquisar Produto")
pesquisa = st.text_input("Digite o nome ou código do produto:").strip().lower()

# ============ FILTRAR RESULTADOS ============
if pesquisa:
    df_filtrado = df[df.astype(str).apply(lambda x: x.str.lower().str.contains(pesquisa)).any(axis=1)]
else:
    df_filtrado = df.copy()

# ============ EXIBIR RESULTADOS ============
if df_filtrado.empty:
    st.warning("Nenhum produto encontrado.")
else:
    for _, row in df_filtrado.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            # Imagem do produto
            nome_imagem = f"{row['DESCRIÇÃO DO PRODUTO']}.jpg"
            try:
                imagem = carregar_imagem(nome_imagem)
            except:
                imagem = carregar_imagem("SEM IMAGEM.jpg")
            col1.image(imagem, use_container_width=True)

            # Informações do produto
            col2.markdown(f"### {row['DESCRIÇÃO DO PRODUTO']}")
            col2.write(f"**Marca:** {row['MARCA']}")
            if not pd.isna(row['COMPRIMENTO']):
                col2.write(f"**Medidas:** {row['COMPRIMENTO']} x {row['LARGURA']} x {row['ALTURA']}")
            if not pd.isna(row['DIAMETRO']):
                col2.write(f"**Diâmetro:** {row['DIAMETRO']}")
            if not pd.isna(row['POR']):
                col2.write(f"💰 **Preço:** R$ {row['POR']}")
            if not pd.isna(row['DE']):
                col2.write(f"~~De: R$ {row['DE']}~~")
            if not pd.isna(row['DESCONTO']):
                col2.write(f"🎯 **Desconto:** {row['DESCONTO']}%")

            st.divider()
