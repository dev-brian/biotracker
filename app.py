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
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CSS PERSONALIZADO — Compatible con Light y Dark mode
# ============================================================================
st.markdown(
    """
    <style>
    /* ===== TIPOGRAFÍA ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ===== VARIABLES DE COLOR (funcionan en ambos modos) ===== */
    :root {
        --bio-primary: #7c3aed;
        --bio-primary-light: #a78bfa;
        --bio-primary-dark: #5b21b6;
        --bio-accent: #4ecdc4;
        --bio-warm: #f59e0b;
        --bio-danger: #ef4444;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(124, 58, 237, 0.2);
    }

    /* ===== BOTONES DE NAVEGACIÓN ===== */
    div[data-testid="stSidebar"] .nav-btn-container .stButton > button {
        width: 100%;
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 12px;
        padding: 0.7rem 1rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        text-align: left;
        margin-bottom: 4px;
    }

    div[data-testid="stSidebar"] .nav-btn-container .stButton > button:hover {
        border-color: var(--bio-primary);
        transform: translateX(4px);
    }

    /* Botón activo */
    div[data-testid="stSidebar"] .nav-btn-active .stButton > button {
        background: linear-gradient(135deg, var(--bio-primary), var(--bio-primary-dark)) !important;
        color: white !important;
        border-color: var(--bio-primary) !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }

    /* ===== MÉTRICAS ===== */
    [data-testid="stMetric"] {
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 12px;
        padding: 1rem;
    }

    /* Dark mode: fondo oscuro para métricas */
    @media (prefers-color-scheme: dark) {
        [data-testid="stMetric"] {
            background: rgba(124, 58, 237, 0.05);
        }
    }

    /* ===== GRADIENT TEXT UTILITY ===== */
    .bio-gradient-text {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 50%, #4ecdc4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ===== CARDS ===== */
    .bio-card {
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
    }

    .bio-card:hover {
        border-color: var(--bio-primary);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.15);
        transform: translateY(-2px);
    }

    /* Dark mode cards */
    @media (prefers-color-scheme: dark) {
        .bio-card {
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(22, 33, 62, 0.8));
        }
    }

    /* Light mode cards */
    @media (prefers-color-scheme: light) {
        .bio-card {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.03), rgba(78, 205, 196, 0.03));
        }
    }

    /* ===== PRO PANEL ===== */
    .pro-panel {
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    @media (prefers-color-scheme: dark) {
        .pro-panel {
            background: rgba(124, 58, 237, 0.05);
        }
    }

    @media (prefers-color-scheme: light) {
        .pro-panel {
            background: rgba(124, 58, 237, 0.02);
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
        <span style="font-size: 2.2rem;">🧬</span><br>
        <span style="
            font-size: 1.5rem;
            font-weight: 700;
        " class="bio-gradient-text">BioTracker</span>
        <p style="font-size: 0.75rem; opacity: 0.5; margin-top: 2px;">Modelado Farmacocinético</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")

# Gestión del estado de navegación
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "inicio"

# Botones de navegación
def cambiar_pagina(pagina):
    st.session_state.pagina_actual = pagina

# Renderizar botones con estilo activo
paginas = {
    "inicio": {"label": "🏠  Inicio", "icon": "🏠"},
    "cafeina": {"label": "☕  Cafeína", "icon": "☕"},
    "creatina": {"label": "💪  Creatina", "icon": "💪"},
}

for key, info in paginas.items():
    is_active = st.session_state.pagina_actual == key
    css_class = "nav-btn-active" if is_active else "nav-btn-container"
    st.sidebar.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
    if st.sidebar.button(info["label"], key=f"nav_{key}", use_container_width=True):
        cambiar_pagina(key)
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

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
