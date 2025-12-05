import os
import sys

# --- CONTEÚDO DO APP.PY (VERSÃO FINAL COM CORREÇÕES VISUAIS) ---
APP_PY_CONTENT = r'''import streamlit as st
import os
import base64
from io import BytesIO

# --- IMPORTS ---
try:
    from PIL import Image, ImageEnhance
except ImportError:
    Image = None

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Herbario Digital - FitoPerform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CACHING DE IMAGENS ---
@st.cache_data
def get_img_as_base64(file_path):
    """Lê uma imagem do disco e converte para base64."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

# --- BACKGROUND PROCESSADO ---
@st.cache_data
def get_processed_background():
    # Tenta usar a imagem gerada (fundo.png) ou a original enviada
    possible_files = ["fundo.png", "Gemini_Generated_Image_ynyy07ynyy07ynyy.png"]
    img_path = next((f for f in possible_files if os.path.exists(f)), None)
    
    if not img_path or Image is None:
        return None
    try:
        img = Image.open(img_path).convert("RGBA")
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.15) # Clarear levemente
        buffered = BytesIO()
        img = img.convert('RGB')
        img.save(buffered, format="JPEG", quality=70)
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception:
        return None

bg_b64 = get_processed_background()

# --- FUNÇÃO LOGO ---
def get_logo_html(image_path, link_url):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        return f'<a href="{link_url}" target="_blank"><img src="data:image/png;base64,{encoded}" class="sidebar-logo"></a>'
    return ""

# --- CSS AVANÇADO (BOTANICAL UI V10 - FINAL) ---
css_background = f"""
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
""" if bg_b64 else """
    .stApp { background-color: #F7F5EB; }
"""

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Fauna+One&display=swap');

    {css_background}
    
    .block-container {{ padding-top: 2rem; padding-bottom: 5rem; }}
    
    /* Header Overlay */
    .header-overlay {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        backdrop-filter: blur(5px);
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.5);
    }}

    /* Tipografia */
    h1 {{ 
        font-family: 'Cinzel', serif !important; 
        color: #1a472a !important; 
        font-size: 3.5rem !important; 
        margin-bottom: 5px !important; 
        text-shadow: none !important; 
    }}
    h2, h3 {{ font-family: 'Cinzel', serif !important; color: #2d5a3f !important; }}
    p, li, span, div, a {{ font-family: 'Fauna One', serif; color: #2c3e50; }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{ background-color: rgba(255, 253, 245, 0.96); border-right: 1px solid #dcdcdc; }}
    .sidebar-logo {{ display: block; margin: 0 auto 20px auto; width: 90%; transition: transform 0.2s; }}
    .sidebar-logo:hover {{ transform: scale(1.05); cursor: pointer; }}

    /* Cards da Home */
    .plant-card-v2 {{ background-color: rgba(255, 255, 255, 0.95); border: 1px solid #dcdcdc; border-radius: 8px 25px 8px 25px; padding: 0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); transition: transform 0.2s ease; height: 100%; overflow: hidden; }}
    .plant-card-v2:hover {{ transform: translateY(-5px); box-shadow: 0 8px 20px rgba(27, 77, 62, 0.2); border-color: #4CAF50; }}
    .card-img-wrapper {{ height: 180px; overflow: hidden; border-bottom: 3px solid #1a472a; background-color: #f4f4f4; }}
    .card-img-v2 {{ width: 100%; height: 100%; object-fit: cover; }}
    .card-body {{ padding: 15px; text-align: center; }}
    
    /* Badges */
    .badge-pill {{ 
        display: inline-block; 
        padding: 6px 14px; 
        border-radius: 50px; 
        font-size: 0.75rem; 
        font-weight: bold; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        color: #FFFFFF !important; 
        background-color: #2e7d32 !important; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.2); 
    }}

    /* Botões */
    div.stButton > button {{ 
        background-color: #1a472a !important; 
        color: #FFFFFF !important; 
        border-radius: 30px; 
        border: 2px solid #1a472a; 
        padding: 8px 20px; 
        font-family: 'Cinzel', serif; 
        font-weight: bold;
        transition: all 0.2s; 
        width: 100%; 
    }}
    div.stButton > button:hover {{ 
        background-color: #2d5a3f !important; 
        color: #FFFFFF !important; 
        border-color: #2d5a3f; 
        transform: scale(1.02);
    }}
    div.stButton > button p {{ color: #FFFFFF !important; }}

    /* --- CARTÃO DE DETALHES TRANSLÚCIDO --- */
    .detail-card {{
        background-color: rgba(255, 255, 255, 0.93); /* Branco translúcido forte */
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 20px;
        height: 100%;
        color: #2c3e50;
    }}

    /* Estilo Polaroid da imagem de detalhes */
    .taped-photo {{ 
        background: white; 
        padding: 10px 10px 40px 10px; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2); 
        transform: rotate(-1.5deg); 
        margin-bottom: 20px; 
        border: 1px solid #ddd;
    }}
    
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# --- CLASSE DE DADOS ---
class Planta:
    def __init__(self, id_planta, nome, nome_cientifico, categoria, descricao, mecanismo, dose, interacoes, adversos, contraindicacoes, nivel_evidencia):
        self.id = id_planta
        self.nome = nome
        self.nome_cientifico = nome_cientifico
        self.categoria = categoria
        self.descricao = descricao
        self.mecanismo = mecanismo
        self.dose = dose
        self.interacoes = interacoes
        self.adversos = adversos
        self.contraindicacoes = contraindicacoes
        self.nivel_evidencia = nivel_evidencia

# --- BANCO DE DADOS ---
PLANTAS = [
    Planta("tribulus", "Tribulus", "Tribulus terrestris L.", "Hormonal", "Espécie rica em saponinas esteroidais.", "Aumento de LH, testosterona e DHEA. Estímulo de NO.", "250 mg, 3x ao dia (45% saponinas).", "Potencializa hormonais e TRH.", "Refluxo, náusea.", "Grávidas, HPB sem controle.", "Moderado"),
    Planta("maca", "Maca Peruana", "Lepidium meyenii Walp.", "Adaptógeno", "Raiz andina nutritiva e tônica.", "Modulação seminal e antioxidante. Inibição da FAAH.", "1,5 a 3 g/dia.", "Interfere em exames hormonais.", "Desconforto digestivo.", "Câncer hormônio-dependente.", "Alto"),
    Planta("ashwagandha", "Ashwagandha", "Withania somnifera", "Adaptógeno / Força", "Ginseng Indiano. Redução de cortisol.", "GABA-mimético, reduz cortisol, aumenta ATP.", "300-600 mg/dia.", "Potencializa sedativos.", "Sonolência, risco tireoidiano.", "Gravidez, doenças autoimunes.", "Alto"),
    Planta("mucuna", "Mucuna", "Mucuna pruriens", "Neuromodulador", "Fonte natural de L-DOPA.", "Aumenta dopamina, reduzindo prolactina.", "400 mg (20% L-DOPA).", "Contraindicado com IMAOs.", "Náusea, discinesia.", "Esquizofrenia, gravidez.", "Moderado"),
    Planta("longjack", "Long Jack", "Eurycoma longifolia", "Hormonal", "Tongkat Ali. Libera testosterona ligada.", "Reduz SHBG e conversão em estrogênio.", "400 mg/dia (euricomanona).", "Reduz absorção de propranolol.", "Raro risco hepático.", "Câncer de próstata.", "Moderado"),
    Planta("serenoa", "Saw Palmetto", "Serenoa repens", "Próstata", "Palmeira anã. Padrão ouro para próstata.", "Inibe 5-alfa-redutase (Testo -> DHT).", "320 mg/dia.", "Risco sangramento.", "Náusea, cefaleia.", "Mulheres em idade fértil.", "Alto"),
    Planta("ajuga", "Turkesterone", "Ajuga turkestanica", "Anabólico Natural", "Rica em ecdisteroides.", "Síntese proteica via receptor ERβ.", "500-2000 mg/dia.", "Sinergia com anabolizantes.", "Segurança alta em estudos curtos.", "Hipersensibilidade.", "Baixo"),
    Planta("prunus", "Pygeum", "Prunus africana", "Próstata", "Cerejeira africana. Anti-inflamatório.", "Inibe proliferação de fibroblastos.", "100-200 mg/dia.", "Seguro.", "Desconforto gástrico raro.", "Crianças.", "Alto"),
    Planta("urtica", "Urtiga", "Urtica dioica", "Próstata / SHBG", "Raiz de urtiga. 'Destrava' a testosterona.", "Liga-se à SHBG.", "300-600 mg/dia.", "Potencializa diuréticos.", "Leve desconforto GI.", "Insuficiência renal/cardíaca.", "Moderado"),
    Planta("feno", "Feno-Grego", "Trigonella foenum-graecum", "Metabólico", "Sementes para libido e glicemia.", "Inibição parcial aromatase. Sensibiliza LH.", "500-600 mg/dia.", "Potencializa insulina.", "Odor corporal característico.", "Gravidez.", "Alto"),
    Planta("tetradium", "Evodia", "Tetradium ruticarpum", "Metabólico", "Wu Zhu Yu. Termogênico.", "Agonista vanilóide.", "5-30 mg/dia (evodiamina).", "Inibe enzimas hepáticas CYP.", "Falta de dados.", "Não recomendado.", "Baixo"),
    Planta("cyanotis", "Cyanotis", "Cyanotis vaga", "Anabólico Natural", "Fonte de Beta-Ecdisterona.", "Similar ao Turkesterone.", "Dose não estabelecida.", "Desconhecidas.", "Falta de estudos.", "Não recomendado.", "Muito Baixo"),
    Planta("kaempferia", "Gengibre Preto", "Kaempferia parviflora", "Vigor", "Ginseng Tailandês. Vasodilatador.", "Inibe PDE5, aumenta NO.", "180-360 mg/dia.", "Cuidado com hipotensores.", "Bem tolerado.", "Crianças.", "Baixo"),
    Planta("bulbine", "Bulbine", "Bulbine latifolia", "Hormonal (Exp)", "Planta africana potente mas arriscada.", "Aumento agudo de testosterona.", "Não segura.", "Altera enzimas renais.", "Hepatotóxico.", "Contraindicado.", "Risco")
]

def change_view(view, plant_id=None):
    st.session_state['view'] = view
    st.session_state['selected_plant_id'] = plant_id

if 'view' not in st.session_state: st.session_state['view'] = 'home'
if 'selected_plant_id' not in st.session_state: st.session_state['selected_plant_id'] = None

# --- SIDEBAR (INFO E CONTATO) ---
with st.sidebar:
    logo_path = "image_ecaac2.png"
    logo_html = get_logo_html(logo_path, "https://www.plantaciencia.com/")
    if logo_html:
        st.markdown(logo_html, unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><a href='https://www.plantaciencia.com/' target='_blank' style='text-decoration: none; color: #1a472a; font-weight: bold;'>Apoio Oficial</a></div>", unsafe_allow_html=True)
    else:
        st.markdown("## FitoPerform")

    with st.expander("👨‍⚕️ Fale com o Farmacêutico", expanded=False):
        st.markdown("""
        <div style="background-color: #fff; border-left: 4px solid #1B4D3E; padding: 15px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-top: 10px; font-size: 0.9em;">
            <strong style="color: #1a472a; font-size: 1.1em;">Thiago Abranches</strong><br>
            <em style="color: #666;">Farmacêutico Clínico</em><br>
            <hr style="margin: 5px 0;">
            <strong>CRF-SP:</strong> 091811<br>
            <strong>CRF-RJ:</strong> 25368<br>
            <br>
            📞 (11) 94146-9952<br>
            ✉️ thiagoabranches.farma@gmail.com
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Autores do Livro")
    st.markdown("""
    <div style="font-size: 0.9em; line-height: 1.6;">
    • <b>Thiago Abranches</b> (MSc. UFRJ)<br>
    • <b>Marina Ramos de Azevedo</b> (DSc. IFRJ)<br>
    • <b>Prof. Dr. Leopoldo C. Baratto</b> (DSc. UFRJ)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Desenvolvedor da versão aplicativo:** Thiago Abranches")
    st.markdown("---")
    
    st.error("⚠️ **Uso profissional**\n\nEste aplicativo é destinado a profissionais prescritores habilitados, seu uso não substitui a avaliação clinica do profissional.")
    
    st.markdown("""
        <a href="https://www.plantaciencia.com/_files/ugd/aedcbc_09803571856343ea82fed6ba99b0b7f2.pdf" target="_blank" style="display: block; width: 100%; padding: 12px; background: linear-gradient(135deg, #1B4D3E 0%, #2D6A4F 100%); color: #FFFFFF !important; text-align: center; border-radius: 8px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.2); margin-top: 10px; margin-bottom: 20px;">
            📥 Baixar Livro (PDF)
        </a>
    """, unsafe_allow_html=True)
    
    st.caption("Copyright © 2025 Thiago Abranches.\nTodos os direitos reservados.")

# ==============================================================================
# VIEW: HOME
# ==============================================================================
if st.session_state['view'] == 'home':
    
    st.markdown("""
    <div class="header-overlay animate-enter">
        <h1 style="color: #1a472a; font-size: 4rem;">HERBARIO DIGITAL</h1>
        <p style="font-size: 1.2rem; color: #1a472a; font-style: italic; margin-top: -10px;">
            Guia de Plantas Medicinais e Desempenho Físico
        </p>
        <div style="width: 100px; height: 3px; background: #1a472a; margin: 20px auto;"></div>
    </div>
    """, unsafe_allow_html=True)

    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Pesquisar", placeholder="Nome da planta...", label_visibility="collapsed")
    with col_filter:
        cat_filter = st.selectbox("Categoria", ["Todas", "Hormonal", "Adaptógeno", "Próstata", "Anabólico Natural", "Metabólico"], label_visibility="collapsed")

    filtered = PLANTAS
    if cat_filter != "Todas": filtered = [p for p in filtered if cat_filter in p.categoria]
    if search: filtered = [p for p in filtered if search.lower() in p.nome.lower() or search.lower() in p.descricao.lower()]

    cols = st.columns(4)
    for idx, plant in enumerate(filtered):
        col = cols[idx % 4]
        
        with col:
            img_path = f"imagens_plantas/{plant.id}.jpg"
            img_b64 = get_img_as_base64(img_path)
            
            if img_b64:
                img_html = f'<img src="data:image/jpeg;base64,{img_b64}" class="card-img-v2">'
            else:
                img_html = f'''
                <div style="height:100%; background:#f0f4f1; display:flex; align-items:center; justify-content:center; flex-direction:column; color:#8ba896;">
                    <div style="font-size:3em;">🌿</div>
                    <div style="font-size:0.8em; font-family:'Cinzel';">Imagem Indisponível</div>
                </div>
                '''

            # Correção de indentação no HTML para evitar blocos de código
            st.markdown(f"""<div class="plant-card-v2 animate-enter" style="animation-delay: {idx * 0.03}s">
<div class="card-img-wrapper">{img_html}</div>
<div class="card-body">
<div class="card-title-v2">{plant.nome}</div>
<span class="card-scientific">{plant.nome_cientifico}</span>
<span class="badge-pill">
{plant.nivel_evidencia}
</span>
</div>
</div>""", unsafe_allow_html=True)
            
            if st.button(f"Ver Detalhes", key=f"btn_{plant.id}"):
                change_view('detail', plant.id)
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# VIEW: DETALHES
# ==============================================================================
elif st.session_state['view'] == 'detail':
    plant = next((p for p in PLANTAS if p.id == st.session_state['selected_plant_id']), None)
    if plant:
        if st.button("← Voltar ao Herbário", key="back_btn"):
            change_view('home')
            st.rerun()

        c1, c2 = st.columns([1, 2])
        
        # Coluna da Imagem (Esquerda)
        with c1:
            img_path = f"imagens_plantas/{plant.id}.jpg"
            img_b64 = get_img_as_base64(img_path)
            
            if img_b64:
                st.markdown(f"""<div class="taped-photo">
<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%;">
<div style="text-align:center; font-family:'Courier New'; font-size:0.8em; margin-top:5px; color:#555;">Fig. 1: {plant.nome}</div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="taped-photo" style="height:300px; display:flex; align-items:center; justify-content:center; background:#f9f9f9; color:#ccc;">
<span>Imagem não carregada</span>
</div>""", unsafe_allow_html=True)
            
            # Info Rápida
            st.markdown(f"""<div class="detail-card">
<h3 style="margin-top:0;">🏷️ Categoria</h3>
<p>{plant.categoria}</p>
<hr style="margin: 15px 0;">
<h3>🧪 Evidência</h3>
<p>{'Nível Alto: Estudos Clínicos Robustos' if plant.nivel_evidencia == 'Alto' else 'Atenção: Risco Elevado' if 'Risco' in plant.nivel_evidencia else f'Nível: {plant.nivel_evidencia}'}</p>
</div>""", unsafe_allow_html=True)

        # Coluna do Texto (Direita) - CORREÇÃO DE INDENTAÇÃO PARA HTML
        with c2:
            st.markdown(f"""<div class="detail-card">
<h1 style="text-align: left; font-size: 3rem !important; color: #1a472a; margin-bottom: 0;">{plant.nome}</h1>
<h3 style="font-style: italic; color: #666 !important; margin-top: -5px; margin-bottom: 20px;">{plant.nome_cientifico}</h3>

<div style='background-color: rgba(26, 71, 42, 0.05); border-left: 4px solid #1a472a; padding: 15px; border-radius: 4px; margin-bottom: 25px; font-size: 1rem; color: #2c3e50;'>
{plant.descricao}
</div>

<h3 style="color: #2d5a3f; margin-bottom: 10px;">⚙️ Mecanismo</h3>
<p style="color: #2c3e50; line-height: 1.6;">{plant.mecanismo}</p>

<div style="margin-top: 20px; padding: 15px; background-color: #e8f5e9; border-radius: 8px; border: 1px solid #c8e6c9;">
<h3 style="margin: 0 0 10px 0; color: #1b5e20;">💊 Dosagem Usual</h3>
<p style="margin: 0; font-weight: bold; color: #1b5e20; font-size: 1.1rem;">{plant.dose}</p>
</div>

<hr style="margin: 30px 0; border-top: 1px solid #ddd;">

<h3 style='color: #8B0000 !important; margin-bottom: 20px;'>⚠️ Perfil de Segurança</h3>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
<div>
<strong>Efeitos Adversos:</strong>
<p style="font-size: 0.95rem; color: #444;">{plant.adversos}</p>
</div>
<div>
<strong>Contraindicações:</strong>
<p style="font-size: 0.95rem; color: #b71c1c;">{plant.contraindicacoes}</p>
</div>
</div>

<div style="margin-top: 20px;">
<strong>Interações:</strong>
<p style="font-size: 0.95rem; color: #444; font-style: italic;">{plant.interacoes}</p>
</div>
</div>""", unsafe_allow_html=True)
'''

# --- SCRIPT DE RESGATE E EXTRAÇÃO ---
RESTAURAR_TUDO_PY = r'''
import fitz  # PyMuPDF
import os
import sys
from PIL import Image

# Força UTF-8 para evitar erros no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Páginas das plantas no PDF
PAGINAS_PLANTAS = {
    "tribulus": 8, "maca": 13, "ashwagandha": 18, "mucuna": 24, "longjack": 29,
    "serenoa": 34, "ajuga": 39, "prunus": 43, "urtica": 48, "feno": 53,
    "tetradium": 58, "cyanotis": 63, "kaempferia": 67, "bulbine": 72
}

def restaurar():
    print("--- INICIANDO RESTAURACAO DO PROJETO ---")

    # 1. Recriar requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("streamlit\nPillow\n")
    print("[OK] requirements.txt criado.")

    # 2. Extrair e Otimizar Imagens
    pdf_nome = "livro pm desempenho fisico 2025.pdf"
    
    if not os.path.exists(pdf_nome):
        print(f"[ERRO] Falta o arquivo '{pdf_nome}'.")
        print("Coloque o PDF na pasta e rode novamente.")
        return

    if not os.path.exists("imagens_plantas"):
        os.makedirs("imagens_plantas")

    try:
        doc = fitz.open(pdf_nome)
        print("[INFO] Extraindo imagens do PDF...")
        
        for planta_id, pagina_num in PAGINAS_PLANTAS.items():
            try:
                if pagina_num < len(doc):
                    page = doc.load_page(pagina_num)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    
                    # Salva direto como JPG Otimizado
                    img_path = f"imagens_plantas/{planta_id}.jpg"
                    
                    # Converte de pixmap para PIL Image para otimizar
                    data = pix.tobytes("ppm")
                    import io
                    img = Image.open(io.BytesIO(data)).convert("RGB")
                    img.thumbnail((800, 1200))
                    img.save(img_path, "JPEG", quality=75, optimize=True)
                    
                    print(f"[OK] Gerado: {img_path}")
                else:
                    print(f"[AVISO] Pagina {pagina_num} nao existe.")
            except Exception as e:
                print(f"[ERRO] {planta_id}: {e}")
                
        print("\n[SUCESSO] Restauracao concluida!")
        print("Agora voce tem 'app.py' (cole o codigo), 'requirements.txt' e a pasta 'imagens_plantas'.")
        
    except Exception as e:
        print(f"[ERRO CRITICO] {e}")

if __name__ == "__main__":
    restaurar()
'''

def criar_script_restauracao():
    with open("restaurar_projeto.py", "w", encoding="utf-8") as f:
        f.write(RESTAURAR_TUDO_PY)
    
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(APP_PY_CONTENT)

    print("[INFO] Scripts criados. Execute 'python restaurar_projeto.py' para recuperar as imagens.")

if __name__ == "__main__":
    criar_script_restauracao()