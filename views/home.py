"""
BioTracker — Página de Inicio
===============================
Landing page promocional del proyecto.
Explica el problema, quiénes lo desarrollan, y para quién es.
"""

import streamlit as st


def render():
    """Renderiza la página de inicio de BioTracker."""

    # ================================================================
    # HERO SECTION
    # ================================================================
    st.markdown(
        """
        <div style="text-align: center; padding: 2.5rem 0 1rem 0;">
            <h1 style="
                font-size: 3.5rem;
                margin-bottom: 0.3rem;
            "><span class="bio-gradient-text"><span class="material-symbols-rounded" style="vertical-align: middle;">science</span> BioTracker</span></h1>
            <p style="font-size: 1.4rem; opacity: 0.8; font-weight: 300;">
                Entiende cómo tu cuerpo procesa lo que consumes
            </p>
            <p style="font-size: 0.95rem; opacity: 0.5; margin-top: 0.5rem;">
                Simulación farmacocinética interactiva basada en matemáticas reales
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ================================================================
    # EL PROBLEMA
    # ================================================================
    st.markdown(
        """
        ### :material/target: El Problema

        Millones de personas consumen **cafeína** y **suplementos deportivos** a diario,
        pero pocas entienden **cuánto tiempo duran sus efectos**, **cuándo alcanzan su pico máximo**,
        o **por qué sienten un bajón de energía** horas después.

        > *¿Alguna vez tomaste un café a las 4 PM y no pudiste dormir a las 11 PM?*
        > *¿Te preguntaste cuántos días necesitas tomar creatina antes de notar resultados?*

        Las respuestas a estas preguntas **se pueden calcular matemáticamente**. El cuerpo humano
        sigue patrones predecibles de absorción y eliminación que las ciencias farmacéuticas
        han modelado durante décadas.
        """
    )

    st.markdown("---")

    # ================================================================
    # LA SOLUCIÓN
    # ================================================================
    st.markdown("### :material/lightbulb: Nuestra Solución")

    st.markdown(
        """
        **BioTracker** es una aplicación que convierte esas ecuaciones científicas en
        **gráficas interactivas** que cualquiera puede entender. Modifica tu dosis, tu peso,
        y observa en tiempo real cómo cambia la curva de concentración en tu cuerpo.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="bio-card">
                <h3 style="margin-top: 0;"><span class="material-symbols-rounded" style="vertical-align: middle;">local_cafe</span> Módulo Cafeína</h3>
                <p style="font-weight: 500; opacity: 0.9;">Efecto Agudo — Pico y Eliminación</p>
                <p style="opacity: 0.7; font-size: 0.9rem;">
                    Visualiza cómo la cafeína se absorbe en tu cuerpo, alcanza su
                    <strong>concentración máxima</strong> (generalmente en ~45 min),
                    y luego se elimina gradualmente. Identifica la
                    <strong>hora exacta del bajón de energía</strong>.
                </p>
                <p class="text-muted" style="margin-top: 1rem;">
                    <span class="material-symbols-rounded" style="vertical-align: middle; font-size: 1rem;">timer</span> Escala: horas · <span class="material-symbols-rounded" style="vertical-align: middle; font-size: 1rem;">show_chart</span> Curva tipo campana
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="bio-card">
                <h3 style="margin-top: 0;"><span class="material-symbols-rounded" style="vertical-align: middle;">fitness_center</span> Módulo Creatina</h3>
                <p style="font-weight: 500; opacity: 0.9;">Efecto Crónico — Saturación Progresiva</p>
                <p style="opacity: 0.7; font-size: 0.9rem;">
                    Simula cómo tus músculos acumulan fosfocreatina día tras día.
                    Compara la <strong>fase de carga</strong> (20g/día, resultados en ~5 días)
                    vs la <strong>fase de mantenimiento</strong> (5g/día, resultados en ~4 semanas).
                </p>
                <p class="text-muted" style="margin-top: 1rem;">
                    <span class="material-symbols-rounded" style="vertical-align: middle; font-size: 1rem;">calendar_today</span> Escala: días/semanas · <span class="material-symbols-rounded" style="vertical-align: middle; font-size: 1rem;">show_chart</span> Curva de saturación
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ================================================================
    # ¿CÓMO FUNCIONA? (Explicación accesible)
    # ================================================================
    st.markdown("---")
    st.markdown(
        """
        ### :material/science: ¿Cómo funciona?

        Cuando consumes una sustancia, tu cuerpo sigue un proceso de **3 etapas**:
        """
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(
            """
            <div class="bio-card" style="text-align: center;">
                <span class="material-symbols-rounded" style="font-size: 2.5rem; color: #4CAF50;">air</span>
                <h4>1. Absorción</h4>
                <p style="font-size: 0.85rem; opacity: 0.7;">
                    La sustancia pasa del estómago al torrente sanguíneo.
                    Cuanto más rápida la absorción, más rápido sientes el efecto.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            """
            <div class="bio-card" style="text-align: center;">
                <span class="material-symbols-rounded" style="font-size: 2.5rem; color: #F44336;">water_drop</span>
                <h4>2. Distribución</h4>
                <p style="font-size: 0.85rem; opacity: 0.7;">
                    La concentración en sangre sube hasta un pico máximo.
                    Este es el momento de mayor efecto.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_c:
        st.markdown(
            """
            <div class="bio-card" style="text-align: center;">
                <span class="material-symbols-rounded" style="font-size: 2.5rem; color: #2196F3;">monitor_heart</span>
                <h4>3. Eliminación</h4>
                <p style="font-size: 0.85rem; opacity: 0.7;">
                    El hígado metaboliza la sustancia y los riñones la excretan.
                    La concentración baja gradualmente.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        BioTracker modela estas etapas usando **ecuaciones diferenciales** — las mismas herramientas
        matemáticas que la industria farmacéutica usa para diseñar medicamentos. Resolvemos estas
        ecuaciones de **dos formas** y las comparamos:

        | Método | ¿Qué hace? | Analogía |
        |:---|:---|:---|
        | **Solución Analítica** (Transformada de Laplace) | Calcula la respuesta matemática *exacta* | Es como saber la receta perfecta de un pastel |
        | **Solución Numérica** (Método de Euler) | Aproxima la respuesta *paso a paso* | Es como probar y ajustar la receta sobre la marcha |

        > La diferencia entre ambas nos muestra qué tan precisa es la aproximación numérica —
        > esto es lo que llamamos **error numérico**, y puedes verlo en cada módulo.
        """
    )

    # ================================================================
    # PARA QUIÉN ES
    # ================================================================
    st.markdown("---")
    st.markdown("### :material/group: ¿Para quién es BioTracker?")

    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        st.markdown(
            """
            <div class="bio-card" style="text-align: center;">
                <span class="material-symbols-rounded" style="font-size: 2rem;">fitness_center</span>
                <h4>Deportistas</h4>
                <p style="font-size: 0.85rem; opacity: 0.7;">
                    Optimiza tus tiempos de consumo de cafeína y creatina
                    según tu peso y actividad.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_p2:
        st.markdown(
            """
            <div class="bio-card" style="text-align: center;">
                <span class="material-symbols-rounded" style="font-size: 2rem;">restaurant</span>
                <h4>Nutricionistas</h4>
                <p style="font-size: 0.85rem; opacity: 0.7;">
                    Herramienta visual para explicar a tus pacientes
                    cómo funcionan los suplementos.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_p3:
        st.markdown(
            """
            <div class="bio-card" style="text-align: center;">
                <span class="material-symbols-rounded" style="font-size: 2rem;">school</span>
                <h4>Estudiantes</h4>
                <p style="font-size: 0.85rem; opacity: 0.7;">
                    Visualiza ecuaciones diferenciales aplicadas a
                    problemas reales del cuerpo humano.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ================================================================
    # SOBRE EL PROYECTO
    # ================================================================
    st.markdown("---")
    st.markdown("### :material/school: Sobre el Proyecto")

    st.markdown(
        """
        BioTracker es el **Proyecto Final** de la materia **Matemáticas para la Ingeniería II**,
        desarrollado por estudiantes de **8° semestre** de la carrera de
        **Ingeniería en Desarrollo y Gestión de Software (IDGS)** en la
        **Universidad Tecnológica de Tlaxcala (UTT)**.

        El objetivo es demostrar que las ecuaciones diferenciales no son solo teoría:
        **tienen aplicaciones directas** en la salud, la nutrición y el deporte.
        """
    )

    # Stack tecnológico (colapsable para no saturar)
    with st.expander(":material/build: Tecnologías utilizadas"):
        st.markdown(
            """
            | Componente | Tecnología | Propósito |
            | :---: | :---: | :---: |
            | Interfaz Web | **Streamlit** | Aplicación interactiva sin necesidad de HTML/JS |
            | Motor Simbólico | **SymPy** | Resolución analítica con Transformada de Laplace |
            | Motor Numérico | **NumPy** | Método de Euler para aproximación paso a paso |
            | Visualización | **Plotly** | Gráficas interactivas con zoom y hover |
            | Lenguaje | **Python 3.11+** | Ecosistema científico robusto |
            """
        )

    # ================================================================
    # PRÓXIMAMENTE
    # ================================================================
    st.markdown("---")
    st.markdown("### :material/update: Próximamente en BioTracker")
    
    col_x, col_y, col_z = st.columns(3)
    with col_x:
        st.markdown(
            """
            <div class="bio-card">
                <h4><span class="material-symbols-rounded" style="vertical-align: middle; font-size: 1.5rem;">medication</span> Más Suplementos</h4>
                <p class="text-muted" style="font-size: 0.9rem; margin-top: 0.5rem;">Módulos de Proteína Whey, Melatonina y Vitaminas D/B12.</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col_y:
        st.markdown(
            """
            <div class="bio-card">
                <h4><span class="material-symbols-rounded" style="vertical-align: middle; font-size: 1.5rem;">watch</span> Smartwatches</h4>
                <p class="text-muted" style="font-size: 0.9rem; margin-top: 0.5rem;">Sincronización de ritmo cardíaco y sueño desde Apple Watch o Garmin.</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col_z:
        st.markdown(
            """
            <div class="bio-card">
                <h4><span class="material-symbols-rounded" style="vertical-align: middle; font-size: 1.5rem;">monitoring</span> Perfil Histórico</h4>
                <p class="text-muted" style="font-size: 0.9rem; margin-top: 0.5rem;">Guarda tu historial de ingesta y observa métricas a largo plazo.</p>
            </div>
            """, unsafe_allow_html=True
        )

    # ================================================================
    # FOOTER
    # ================================================================
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; opacity: 0.7; font-size: 1.05rem; padding: 1rem 0; line-height: 1.6;">
            BioTracker v1.0 — Proyecto Final · Matemáticas para la Ingeniería II<br>
            Universidad Tecnológica de Tlaxcala · 8° Semestre IDGS · Abril 2026<br>
            <br>
            <em>← Selecciona un módulo en el menú lateral para comenzar</em>
        </div>
        """,
        unsafe_allow_html=True,
    )
