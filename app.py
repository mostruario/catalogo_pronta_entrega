import streamlit as st
import pandas as pd
import os

# --- Configuração da página ---
st.set_page_config(page_title="Catálogo - Pronta Entrega", layout="wide")

# --- Carregar logo ---
logo_path = "STATIC/IMAGENS/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
else:
    st.warning("Logo não encontrada.")

# --- Título ---
st.markdown("<h1 style='text-align: center;'>CATÁLOGO - PRONTA ENTREGA</h1>", unsafe_allow_html=True)

# --- Carregar planilha ---
df = pd.read_excel("ESTOQUE PRONTA ENTREGA CLAMI.xlsx", header=1)

# --- Ajuste do caminho das imagens ---
def ajustar_caminho_imagem(caminho):
    if pd.isna(caminho):
        return "STATIC/IMAGENS/SEM IMAGEM.jpg"
    nome_arquivo = os.path.basename(str(caminho))
    return f"STATIC/IMAGENS/{nome_arquivo}"

df['LINK_IMAGEM'] = df['LINK_IMAGEM'].apply(ajustar_caminho_imagem)

# --- Filtros de pesquisa ---
col1, col2 = st.columns([1, 2])

with col1:
    marca_selecionada = st.selectbox("Marca", options=[""] + sorted(df["Marca"].dropna().unique().tolist()))
with col2:
    pesquisa = st.text_input("Pesquisar Produto")

# --- Aplicar filtros ---
df_filtrado = df.copy()
if marca_selecionada:
    df_filtrado = df_filtrado[df_filtrado["Marca"] == marca_selecionada]
if pesquisa:
    df_filtrado = df_filtrado[df_filtrado["Descrição"].str.contains(pesquisa, case=False, na=False)]

# --- Contador de produtos ---
st.markdown(f"**Total de produtos exibidos:** {len(df_filtrado)}")

# --- Exibir produtos ---
cols = st.columns(5)

for idx, (_, row) in enumerate(df_filtrado.iterrows()):
    col = cols[idx % 5]
    with col:
        st.markdown("<div style='margin-bottom: 20px;'>", unsafe_allow_html=True)
        try:
            st.image(row["LINK_IMAGEM"], use_container_width=True)
        except:
            st.image("STATIC/IMAGENS/SEM IMAGEM.jpg", use_container_width=True)

        st.markdown(f"**{row['Descrição']}**", unsafe_allow_html=True)
        st.markdown(f"<small><b>Código:</b> {row['Código']}</small>", unsafe_allow_html=True)
        st.markdown(f"<small><b>Marca:</b> {row['Marca']}</small>", unsafe_allow_html=True)
        st.markdown(f"<small><b>Comp.:</b> {row['Comp.']}, <b>Alt.:</b> {row['Alt.']}, <b>Larg.:</b> {row['Larg.']}</small>", unsafe_allow_html=True)
        st.markdown(f"<small><b>De:</b> R$ {row['Preço De']}</small>", unsafe_allow_html=True)
        st.markdown(f"<small><b>Por:</b> <span style='color:red;'>R$ {row['Preço Por']}</span></small>", unsafe_allow_html=True)
        st.markdown(f"<small><b>Estoque:</b> {row['Estoque']}</small>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
