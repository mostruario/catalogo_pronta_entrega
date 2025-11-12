import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO

# ------------------ CONFIGURAÇÃO ------------------
st.set_page_config(page_title="Catálogo - Pronta Entrega", layout="wide")
BASE_DIR = Path(__file__).resolve().parent
DEBUG = False

# ------------------ LOGO ------------------
logo_path = BASE_DIR / "STATIC" / "IMAGENS" / "logo.png"
if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
else:
    logo_b64 = ""

st.markdown(
    f"""
    <div style="display:flex; align-items:center; justify-content:flex-start; margin-bottom:10px;">
        <img src="data:image/png;base64,{logo_b64}" style="width:90px; height:auto; object-fit:contain;">
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 style="text-align:center;">CATÁLOGO - PRONTA ENTREGA</h1>', unsafe_allow_html=True)

# ------------------ PLANILHA ------------------
DATA_PATH = BASE_DIR / "ESTOQUE PRONTA ENTREGA CLAMI.xlsx"
if not DATA_PATH.exists():
    st.error("❌ Arquivo da planilha não encontrado no diretório do projeto.")
    st.stop()

df = pd.read_excel(DATA_PATH, header=1)
df.columns = df.columns.str.strip()
df = df.drop_duplicates(subset="CODIGO DO PRODUTO", keep="first")

# ------------------ FILTROS ------------------
col1, col2 = st.columns([2, 3])

with col1:
    marca_filter = st.multiselect("Marca", options=df["MARCA"].dropna().unique())

with col2:
    search_term = st.text_input("Pesquisar Produto")

if marca_filter:
    df_filtered = df[df["MARCA"].isin(marca_filter)]
else:
    df_filtered = df.copy()

if search_term:
    df_filtered = df_filtered[df_filtered["DESCRIÇÃO DO PRODUTO"].str.contains(search_term, case=False, na=False)]

st.write(f"Total de produtos exibidos: {len(df_filtered)}")

# ------------------ CONFIG IMAGENS ------------------
IMAGES_DIR = BASE_DIR / "STATIC" / "IMAGENS"
GITHUB_USER = "mostruario"  # link corrigido
GITHUB_REPO = "catalogo_pronta_entrega"
GITHUB_BRANCH = "main"

# ------------------ CARDS ------------------
num_cols = 5
for i in range(0, len(df_filtered), num_cols):
    cols = st.columns(num_cols)
    for j, idx in enumerate(range(i, min(i + num_cols, len(df_filtered)))):
        row = df_filtered.iloc[idx]
        with cols[j]:
            # ---------- IMAGEM ----------
            img_html_src = ""
            img_name = None

            if "LINK_IMAGEM" in row and pd.notna(row["LINK_IMAGEM"]):
                img_name = Path(str(row["LINK_IMAGEM"])).name.strip()

            if img_name:
                local_path = IMAGES_DIR / img_name
            else:
                local_path = IMAGES_DIR / "SEM IMAGEM.jpg"

            if local_path.exists():
                with open(local_path, "rb") as f:
                    img_b64 = base64.b64encode(f.read()).decode()
                    img_html_src = f"data:image/png;base64,{img_b64}"
            else:
                if img_name:
                    img_name_encoded = str(img_name).replace(" ", "%20")
                    img_html_src = (
                        f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/"
                        f"{GITHUB_BRANCH}/STATIC/IMAGENS/{img_name_encoded}"
                    )
                else:
                    img_html_src = (
                        f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/"
                        f"{GITHUB_BRANCH}/STATIC/IMAGENS/SEM%20IMAGEM.jpg"
                    )

            # ---------- PREÇOS ----------
            def to_float(val):
                try:
                    return float(str(val).replace(",", "."))
                except:
                    return 0

            de_valor = f"R$ {to_float(row.get('DE', 0)):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
            por_valor = f"R$ {to_float(row.get('POR', 0)):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

            # ---------- DIMENSÕES ----------
            dimensoes = []
            if row.get("COMPRIMENTO") not in [None, 0, "0", ""]:
                dimensoes.append(f"Comp.: {row['COMPRIMENTO']}")
            if row.get("ALTURA") not in [None, 0, "0", ""]:
                dimensoes.append(f"Alt.: {row['ALTURA']}")
            if row.get("LARGURA") not in [None, 0, "0", ""]:
                dimensoes.append(f"Larg.: {row['LARGURA']}")
            if row.get("DIAMETRO") not in [None, 0, "0", ""]:
                dimensoes.append(f"Ø Diam: {row['DIAMETRO']}")
            dimensoes_str = ", ".join(dimensoes)

            # ---------- CARD ----------
            st.markdown(
                f"""
                <div style="
                    border:1px solid #e0e0e0;
                    border-radius:15px;
                    margin:5px;
                    box-shadow:0 4px 12px rgba(0,0,0,0.15);
                    background-color:#fff;
                    display:flex;
                    flex-direction:column;
                    justify-content:flex-start;
                    height:800px;
                    overflow:hidden;
                ">
                    <div style="text-align:center;">
                        <img src="{img_html_src}" style="width:100%; height:auto; object-fit:cover; border-radius:15px 15px 0 0;">
                    </div>
                    <div style="padding:10px; text-align:left;">
                        <h4 style="margin-bottom:5px; font-size:18px;">{row.get('DESCRIÇÃO DO PRODUTO','')}</h4>
                        <p style="margin:0;"><b>Código:</b> {row.get('CODIGO DO PRODUTO','')}</p>
                        <p style="margin:0;"><b>Marca:</b> {row.get('MARCA','')}</p>
                        <p style="margin:0;">{dimensoes_str}</p>
                        <p style="margin:0;"><b>De:</b> 
                            <span style="text-decoration:line-through; color:#999;">{de_valor}</span></p>
                        <p style="margin:0;"><b>Por:</b> 
                            <span style="color:#d32f2f; font-size:20px; font-weight:bold;">{por_valor}</span></p>
                        <p style="margin:0;"><b>Estoque:</b> {row.get('ESTOQUE DISPONIVEL','')}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )



