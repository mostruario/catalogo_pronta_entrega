# app.py
import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
import base64
from io import BytesIO

# ---------- CONFIGURAÇÃO ----------
st.set_page_config(page_title="Catálogo - Pronta Entrega", layout="wide")

# ---------- CAMINHOS RELATIVOS ----------
BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "logo.png"
DATA_PATH = BASE_DIR / "ESTOQUE PRONTA ENTREGA CLAMI.xlsx"
IMAGES_DIR = BASE_DIR / "IMAGENS"

# ---------- LOGO ----------
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <div style="display:flex; align-items:center; justify-content:flex-start; margin-bottom:10px;">
        <img src="data:image/png;base64,{logo_b64}" 
             style="width:90px; height:auto; object-fit:contain;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 style="text-align: center;">CATÁLOGO - PRONTA ENTREGA</h1>', unsafe_allow_html=True)

# ---------- CARREGAR PLANILHA ----------
df = pd.read_excel(DATA_PATH, header=1)
df.columns = df.columns.str.strip()
df = df.drop_duplicates(subset="CODIGO DO PRODUTO", keep="first")

# ---------- FILTROS ----------
col1, col2 = st.columns([2, 3])
with col1:
    marca_filter = st.multiselect("Marca", options=df["MARCA"].unique())
with col2:
    search_term = st.text_input("Pesquisar Produto")

if marca_filter:
    df_filtered = df[df["MARCA"].isin(marca_filter)]
else:
    df_filtered = df.copy()

if search_term:
    df_filtered = df_filtered[df_filtered["DESCRIÇÃO DO PRODUTO"].str.contains(search_term, case=False, na=False)]

st.write(f"Total de produtos exibidos: {len(df_filtered)}")

# ---------- EXIBIR PRODUTOS ----------
num_cols = 5
for i in range(0, len(df_filtered), num_cols):
    cols = st.columns(num_cols)
    for j, idx in enumerate(range(i, min(i + num_cols, len(df_filtered)))):
        row = df_filtered.iloc[idx]

        # 🔧 Corrige caminho da imagem — extrai só o nome do arquivo
        img_name_raw = row.get("LINK_IMAGEM", "")
        img_name = Path(str(img_name_raw)).name if pd.notna(img_name_raw) else None

        if img_name:
            img_path = IMAGES_DIR / img_name
            if not img_path.exists():
                img_path = IMAGES_DIR / "SEM IMAGEM.jpg"
        else:
            img_path = IMAGES_DIR / "SEM IMAGEM.jpg"

        image = Image.open(img_path)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        de_raw = row.get('DE', 0)
        por_raw = row.get('POR', 0)
        try:
            de_valor = f"R$ {float(str(de_raw).replace(',', '.')):,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
        except:
            de_valor = "R$ 0,00"
        try:
            por_valor = f"R$ {float(str(por_raw).replace(',', '.')):,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
        except:
            por_valor = "R$ 0,00"

        dimensoes = []
        for campo, nome in [('COMPRIMENTO', 'Comp.'), ('ALTURA', 'Alt.'), ('LARGURA', 'Larg.'), ('DIAMETRO', 'Ø Diam.')]:
            valor = row.get(campo)
            if valor not in [None, 0, '0', '']:
                dimensoes.append(f"{nome}: {valor}")
        dimensoes_str = ', '.join(dimensoes)

        st.markdown(
            f"""
            <div style="
                border:1px solid #e0e0e0;
                border-radius:15px;
                margin:5px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                background-color:#ffffff;
                display:flex;
                flex-direction:column;
                justify-content:flex-start;
                height:800px;
                overflow:hidden;
            ">
                <div style="text-align:center;">
                    <img src="data:image/png;base64,{img_str}" 
                         style="width:100%; height:auto; object-fit:cover; border-radius:15px 15px 0 0;">
                </div>
                <div style="padding:10px; text-align:left;">
                    <h4 style="margin-bottom:5px; font-size:18px;">{row['DESCRIÇÃO DO PRODUTO']}</h4>
                    <p style="margin:0;"><b>Código:</b> {row['CODIGO DO PRODUTO']}</p>
                    <p style="margin:0;"><b>Marca:</b> {row['MARCA']}</p>
                    <p style="margin:0;">{dimensoes_str}</p>
                    <p style="margin:0;"><b>De:</b> <span style="text-decoration: line-through; color: #999;">{de_valor}</span></p>
                    <p style="margin:0;"><b>Por:</b> <span style="color:#d32f2f; font-size:20px; font-weight:bold;">{por_valor}</span></p>
                    <p style="margin:0;"><b>Estoque:</b> {row.get('ESTOQUE DISPONIVEL','')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
