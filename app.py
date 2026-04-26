"""
BioTracker — Aplicación Principal
===================================
Modelado Farmacocinético con Ecuaciones Diferenciales.

Punto de entrada de la aplicación Streamlit.
Ejecutar con: python run.py
"""

import streamlit as st

# ============================================================================
# CONFIGURACIÓN DE PÁGINA (debe ser lo primero)
# ============================================================================
st.set_page_config(
    page_title="BioTracker — Modelado Farmacocinético",
    page_icon=":material/health_and_safety:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CSS PERSONALIZADO — Compatible con Light y Dark mode
# ============================================================================
st.markdown(
    """
    <style>
    /* ===== TIPOGRAFÍA E ICONOS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    .material-symbols-rounded {
      font-family: 'Material Symbols Rounded';
      font-weight: normal;
      font-style: normal;
      font-size: 24px;
      line-height: 1;
      letter-spacing: normal;
      text-transform: none !important;
      display: inline-block;
      white-space: nowrap;
      word-wrap: normal;
      direction: ltr;
      -webkit-font-feature-settings: 'liga';
      -webkit-font-smoothing: antialiased;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ===== TABLAS ===== */
    [data-testid="stMarkdownContainer"] table {
        margin-left: auto;
        margin-right: auto;
    }

    [data-testid="stMarkdownContainer"] th {
        text-align: center !important;
    }
    
    [data-testid="stMarkdownContainer"] td {
        text-align: center !important;
    }

    /* ===== VARIABLES DE COLOR (funcionan en ambos modos) ===== */
    :root {
        --bio-primary: #4CAF50;
        --bio-primary-light: #81C784;
        --bio-primary-dark: #388E3C;
        --bio-accent: #2196F3;
        --bio-warm: #FF9800;
        --bio-danger: #F44336;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(76, 175, 80, 0.2);
    }
    
    /* ===== BOTÓN DE COLAPSO (Sidebar) ===== */
    [data-testid="collapsedControl"] {
        color: var(--bio-primary) !important;
        background-color: rgba(76, 175, 80, 0.1) !important;
        border-radius: 50% !important;
        transition: all 0.3s ease;
        padding: 0.2rem !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background-color: var(--bio-primary) !important;
        color: white !important;
    }
    
    /* Reemplazar el icono SVG nativo por un Material Symbol usando pseudo-elemento */
    [data-testid="collapsedControl"] svg {
        display: none !important;
    }
    
    [data-testid="collapsedControl"]::after {
        content: "menu_open";
        font-family: 'Material Symbols Rounded';
        font-size: 24px;
        line-height: 1;
    }

    [data-testid="collapsedControl"][aria-expanded="false"]::after {
        content: "menu";
    }

    /* ===== BOTONES DE NAVEGACIÓN ===== */
    /* Botones inactivos (Secondary por defecto) */
    [data-testid="stSidebar"] div.stButton > button {
        width: 100%;
        border: 1px solid rgba(76, 175, 80, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        text-align: left !important;
        margin-bottom: 4px !important;
        background-color: transparent !important;
        color: inherit;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        border-color: var(--bio-primary) !important;
        transform: translateX(4px) !important;
    }

    /* Botón activo (Primary override) */
    [data-testid="stSidebar"] div.stButton > button[kind="primary"],
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, var(--bio-primary), var(--bio-primary-dark)) !important;
        background-color: transparent !important;
        color: white !important;
        border: 1px solid var(--bio-primary) !important;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3) !important;
    }

    /* ===== MÉTRICAS ===== */
    [data-testid="stMetric"] {
        border: 1px solid rgba(76, 175, 80, 0.15);
        border-radius: 12px;
        padding: 1rem;
    }

    /* Dark mode: fondo oscuro para métricas */
    @media (prefers-color-scheme: dark) {
        [data-testid="stMetric"] {
            background: rgba(76, 175, 80, 0.05);
        }
    }

    /* ===== GRADIENT TEXT UTILITY ===== */
    .bio-gradient-text {
        background: linear-gradient(135deg, #4CAF50 0%, #81C784 50%, #2196F3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ===== CARDS ===== */
    .bio-card {
        border: 1px solid rgba(76, 175, 80, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
        background-color: var(--secondary-background-color);
    }

    .bio-card:hover {
        border-color: var(--bio-primary);
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.15);
        transform: translateY(-2px);
    }

    /* ===== PRO PANEL ===== */
    .pro-panel {
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    @media (prefers-color-scheme: dark) {
        .pro-panel {
            background: rgba(76, 175, 80, 0.05);
        }
    }

    @media (prefers-color-scheme: light) {
        .pro-panel {
            background: rgba(76, 175, 80, 0.02);
        }
    }

    /* ===== MUTED TEXT (works in both modes) ===== */
    .text-muted {
        opacity: 0.6;
        font-size: 0.85rem;
    }

    .text-accent {
        color: var(--bio-primary-light);
        font-weight: 600;
    }

    /* ===== DIVIDERS ===== */
    hr {
        opacity: 0.15 !important;
    }

    /* ===== DATAFRAMES ===== */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ===== EXPANDER STYLING ===== */
    .streamlit-expanderHeader {
        font-weight: 600;
        border-radius: 8px;
    }

    /* ===== RESPONSIVE — TABLET (≤1024px) ===== */
    @media (max-width: 1024px) {
        /* Reducir padding general */
        .block-container {
            padding: 1rem 1.5rem !important;
        }

        /* Cards más compactas */
        .bio-card {
            padding: 1.2rem;
            border-radius: 12px;
        }

        /* Métricas: fuente más pequeña */
        [data-testid="stMetric"] {
            padding: 0.7rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
    }

    /* ===== RESPONSIVE — MÓVIL (≤768px) ===== */
    @media (max-width: 768px) {
        /* Reducir padding en móvil */
        .block-container {
            padding: 0.5rem 0.8rem !important;
        }

        /* Títulos más pequeños */
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.4rem !important; }
        h3 { font-size: 1.15rem !important; }
        h4 { font-size: 1rem !important; }

        /* Hero text smaller */
        .bio-gradient-text {
            font-size: 2.2rem !important;
        }

        /* Cards adaptadas */
        .bio-card {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 0.5rem;
        }

        .bio-card h3 {
            font-size: 1.05rem !important;
        }

        .bio-card h4 {
            font-size: 0.95rem !important;
        }

        .bio-card p {
            font-size: 0.82rem !important;
        }

        /* Métricas compactas en móvil */
        [data-testid="stMetric"] {
            padding: 0.5rem;
            border-radius: 8px;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.1rem !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.72rem !important;
        }

        /* Plotly charts: menor altura */
        [data-testid="stPlotlyChart"] > div {
            max-height: 350px;
        }

        /* Tablas más compactas */
        [data-testid="stDataFrame"] {
            font-size: 0.75rem !important;
        }

        /* Pro panel compacto */
        .pro-panel {
            padding: 0.8rem;
            margin: 0.5rem 0;
        }

        /* LaTeX más pequeño */
        .katex { font-size: 0.85rem !important; }

        /* Sidebar en móvil: menos padding */
        [data-testid="stSidebar"] > div:first-child {
            padding: 0.5rem 0.8rem;
        }

        /* Ocultar texto largo en tooltips en móvil */
        .text-muted {
            font-size: 0.75rem;
        }

        /* Alertas compactas */
        [data-testid="stAlert"] {
            padding: 0.6rem 0.8rem !important;
            font-size: 0.85rem !important;
        }
    }

    /* ===== RESPONSIVE — MÓVIL PEQUEÑO (≤480px) ===== */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.3rem 0.5rem !important;
        }

        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }

        .bio-gradient-text {
            font-size: 1.8rem !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 0.95rem !important;
        }

        .katex { font-size: 0.78rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# NAVEGACIÓN CON BOTONES EN EL SIDEBAR
# ============================================================================
from views import home, caffeine_view, creatine_view

# Logo y título
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <br>
        <span style="
            font-size: 1.5rem;
            font-weight: 700;
        " class="bio-gradient-text"><span class="material-symbols-rounded" style="vertical-align: middle;">science</span> BioTracker</span>
        <p style="font-size: 0.75rem; opacity: 0.5; margin-top: 2px;">Modelado Farmacocinético</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")

if "dark_mode_active" not in st.session_state:
    st.session_state.dark_mode_active = False

st.session_state.dark_mode_active = st.sidebar.toggle("🌙 Modo Oscuro (Glass)", value=st.session_state.dark_mode_active)

if st.session_state.dark_mode_active:
    st.markdown("""
    <style>
    /* DEEP SPACE BACKGROUND */
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #0F172A !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0B1120 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* TEXT COLORS */
    html, body, p, span, h1, h2, h3, h4, h5, h6, label, [class*="css"], .katex {
        color: #F8FAFC !important;
    }
    .text-muted, p.text-muted, [data-testid="stSidebar"] p {
        color: #94A3B8 !important;
    }
    
    /* GRADIENT PRIMARIO (Vitalidad) */
    .bio-gradient-text {
        background: linear-gradient(135deg, #10B981, #0EA5E9) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    /* GLASSMORFISMO (Tarjetas y Contenedores) */
    .bio-card, [data-testid="stMetric"], .pro-panel, [data-testid="stExpander"] > details {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
        border-radius: 16px !important;
    }
    
    [data-testid="stExpander"] details summary {
        background-color: transparent !important;
    }

    /* Botones inactivos (Secondary por defecto) */
    .stApp [data-testid="stSidebar"] div.stButton > button.e7msn5c2 *,
    .stApp [data-testid="stSidebar"] div.stButton > button.st-emotion-cache-gmnumv * {
        background-color: transparent !important;
        color: #F8FAFC !important;
    }
    .stApp [data-testid="stSidebar"] div.stButton > button.e7msn5c2,
    .stApp [data-testid="stSidebar"] div.stButton > button.st-emotion-cache-gmnumv {
        background: #1E293B !important;
        background-color: #1E293B !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .stApp [data-testid="stSidebar"] div.stButton > button.e7msn5c2:hover,
    .stApp [data-testid="stSidebar"] div.stButton > button.st-emotion-cache-gmnumv:hover {
        background: #334155 !important;
        background-color: #334155 !important;
        border-color: #10B981 !important;
        transform: none !important;
    }

    /* Botones Sidebar Override (Primary activo) */
    .stApp [data-testid="stSidebar"] div.stButton > button.e7msn5c1,
    .stApp [data-testid="stSidebar"] div.stButton > button.st-emotion-cache-14vfvr3 {
        background: linear-gradient(135deg, #10B981, #0EA5E9) !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    .stApp [data-testid="stSidebar"] div.stButton > button.e7msn5c1 *,
    .stApp [data-testid="stSidebar"] div.stButton > button.st-emotion-cache-14vfvr3 * {
        background-color: transparent !important;
        color: #FFFFFF !important;
    }
    
    /* Fix Tablas */
    [data-testid="stMarkdownContainer"] table, [data-testid="stTable"] table {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border-collapse: collapse !important;
    }
    [data-testid="stMarkdownContainer"] table th, 
    [data-testid="stMarkdownContainer"] table td,
    [data-testid="stTable"] table th,
    [data-testid="stTable"] table td {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #F8FAFC !important;
        padding: 0.75rem !important;
    }
    [data-testid="stMarkdownContainer"] table th,
    [data-testid="stTable"] table th {
        background-color: rgba(255, 255, 255, 0.06) !important;
    }

    /* Fix Inputs y Selectbox (Dropdowns) */
    .stApp div[data-baseweb="select"] > div,
    .stApp div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #F8FAFC !important;
    }
    .stApp div[data-baseweb="select"] span,
    .stApp div[data-baseweb="input"] input {
        color: #F8FAFC !important;
    }
    .stApp div[data-baseweb="select"] svg {
        fill: #94A3B8 !important;
    }
    
    /* Popover/Lista del Selectbox (Aparece al final del body) */
    /* 1. Limpiar todos los fondos blancos profundamente anidados */
    div[data-baseweb="popover"] * {
        background-color: transparent !important;
        color: #F8FAFC !important;
    }
    
    /* 2. Asignar el fondo oscuro al contenedor principal */
    div[data-baseweb="popover"] > div {
        background-color: #0F172A !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }

    /* 3. Estilos de hover para las opciones individuales */
    div[data-baseweb="popover"] li[role="option"] {
        border-radius: 4px !important;
        margin-bottom: 2px !important;
    }
    div[data-baseweb="popover"] li[role="option"]:hover,
    div[data-baseweb="popover"] li[role="option"][aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    /* Asegurar que el hover aplique incluso si hay spans internos */
    div[data-baseweb="popover"] li[role="option"]:hover *,
    div[data-baseweb="popover"] li[role="option"][aria-selected="true"] * {
        background-color: transparent !important;
    }

    /* Fix Sliders */
    div[data-testid="stSlider"] div {
        color: #F8FAFC !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Gestión del estado de navegación
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "inicio"

# Botones de navegación
def cambiar_pagina(pagina):
    st.session_state.pagina_actual = pagina

# Renderizar botones con estilo activo
paginas = {
    "inicio": {"label": ":material/home:  Inicio", "icon": ":material/home:"},
    "cafeina": {"label": ":material/local_cafe:  Cafeína", "icon": ":material/local_cafe:"},
    "creatina": {"label": ":material/fitness_center:  Creatina", "icon": ":material/fitness_center:"},
}

for key, info in paginas.items():
    is_active = st.session_state.pagina_actual == key
    btn_type = "primary" if is_active else "secondary"
    if st.sidebar.button(info["label"], key=f"nav_{key}", use_container_width=True, type=btn_type):
        cambiar_pagina(key)
        st.rerun()

st.sidebar.markdown("---")

# ============================================================================
# RENDERIZAR PÁGINA SELECCIONADA
# ============================================================================
if st.session_state.pagina_actual == "inicio":
    home.render()
elif st.session_state.pagina_actual == "cafeina":
    caffeine_view.render()
elif st.session_state.pagina_actual == "creatina":
    creatine_view.render()
