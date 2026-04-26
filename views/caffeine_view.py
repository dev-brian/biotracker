"""
BioTracker — Vista del Módulo de Cafeína (v2)
===============================================
Interfaz mejorada con doble método de entrada:
  1. Manual — Slider libre de mg
  2. Catálogo de Productos — Selección desde la base de datos completa

Incluye tarjeta informativa del producto seleccionado, simulación
farmacocinética con Laplace/Euler, y Modo Pro.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from functools import partial

from models import caffeine
from models import caffeine_data
from models.solvers import euler_method, calcular_errores


def render():
    """Renderiza la página completa del módulo de cafeína."""

    st.header(":material/local_cafe: Cafeína — ¿Cuánto dura el efecto?")
    st.markdown(
        "La cafeína es un **alcaloide del grupo de las xantinas** que actúa como "
        "**antagonista de los receptores de adenosina** en el cerebro. "
        "Al bloquear la adenosina (que provoca sedación), estimula el sistema nervioso "
        "central y evita la aparición de fatiga y somnolencia."
    )

    # ================================================================
    # PARÁMETROS INLINE (Expander principal)
    # ================================================================
    with st.expander(":material/settings: Ajuste de Parámetros Biométricos", expanded=True):
        col_method, col_dose, col_weight = st.columns([1.5, 1, 1])
        
        with col_method:
            metodo = st.radio(
                "Método de ingreso",
                [":material/edit: Manual", ":material/menu_book: Catálogo de Productos"],
                help="Manual: ingresa la dosis libremente. Catálogo: elige un producto real y usa su dosis."
            )

        # ------ Método: Catálogo de Productos ------
        if metodo == ":material/menu_book: Catálogo de Productos":
            col_cat, col_prod = st.columns(2)
            with col_cat:
                tipo_absorcion = st.selectbox(
                    "Tipo de absorción",
                    list(caffeine_data.CATEGORIAS.keys()),
                    help="Natural: café, té, chocolate · Sintética: pastillas, pre-workouts · Lenta: liberación sostenida"
                )
                st.caption(caffeine_data.CATEGORIAS[tipo_absorcion]["descripcion"])

            with col_prod:
                productos_cat = caffeine_data.obtener_nombres_por_categoria(tipo_absorcion)
                producto_nombre = st.selectbox("Producto", productos_cat)

            producto = caffeine_data.obtener_producto(producto_nombre)

            with col_dose:
                # Slider acotado al rango del producto
                dosis = st.slider(
                    f"Dosis ({producto['mg_min']}-{producto['mg_max']} mg)",
                    min_value=producto["mg_min"],
                    max_value=max(producto["mg_max"], producto["mg_min"] + 1),
                    value=int(caffeine_data.dosis_promedio(producto)),
                    step=5,
                    help=f"Rango típico para {producto['nombre']}. Dosis recomendada: {producto['dosis_recomendada']}"
                )

            # Factor de absorción del producto
            ka_base = caffeine.KA_DEFAULT * producto["ka_factor"]

        # ------ Método: Manual ------
        else:
            producto = None
            with col_dose:
                dosis = st.slider(
                    "¿Cuánta cafeína consumiste? (mg)",
                    min_value=50, max_value=400, value=200, step=25,
                    help="Café filtrado: ~95 mg · Espresso: ~63 mg · Energy drink: ~80-160 mg · Pastilla: ~200 mg"
                )
            ka_base = caffeine.KA_DEFAULT

        with col_weight:
            peso = st.slider(
                "Tu peso corporal (kg)",
                min_value=40, max_value=120, value=70, step=5,
                help="Tu peso afecta qué tan concentrada queda la cafeína en tu sangre."
            )

        # Parámetros avanzados (colapsados por defecto)
        with st.expander(":material/tune: Parámetros avanzados"):
            col_adv1, col_adv2, col_adv3, col_adv4 = st.columns(4)
            with col_adv1:
                ka = st.slider(
                    "Velocidad de absorción (k_a)",
                    min_value=0.5, max_value=10.0, value=float(round(ka_base, 2)), step=0.1,
                    help="Qué tan rápido pasa la cafeína del estómago a la sangre. Mayor = más rápido. "
                         "Se ajusta automáticamente al seleccionar un producto."
                )

            with col_adv2:
                ke = st.slider(
                    "Velocidad de eliminación (k_e)",
                    min_value=0.05, max_value=0.30, value=caffeine.KE_DEFAULT, step=0.001,
                    format="%.3f",
                    help="Qué tan rápido tu hígado procesa la cafeína. Varía por genética."
                )

            with col_adv3:
                dt = st.slider(
                    "Precisión de Euler (dt)",
                    min_value=0.01, max_value=1.0, value=0.1, step=0.01,
                    help="Tamaño del paso del método numérico. Menor = más preciso."
                )

            with col_adv4:
                duracion = st.slider(
                    "Horas a simular",
                    min_value=6, max_value=48, value=24, step=1
                )

    # Usar defaults si no se abrió el expander
    if 'ka' not in dir():
        ka = ka_base
    if 'ke' not in dir():
        ke = caffeine.KE_DEFAULT
    if 'dt' not in dir():
        dt = 0.1
    if 'duracion' not in dir():
        duracion = 24

    vida_media = np.log(2) / ke

    # ================================================================
    # TARJETA INFORMATIVA DEL PRODUCTO (solo en modo catálogo)
    # ================================================================
    if producto:
        cat_color = caffeine_data.CATEGORIAS[tipo_absorcion]["color"]

        st.markdown(
            f"""
            <div class="bio-card" style="border-left: 4px solid {cat_color}; margin-bottom: 1.5rem; padding: 1.5rem;">
                <h3 style="margin-top: 0; color: inherit;">{producto['nombre']}</h3>
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
                    <div style="flex: 1; min-width: 200px;">
                        <span style="
                            background: {cat_color}22;
                            color: {cat_color};
                            padding: 2px 10px;
                            border-radius: 12px;
                            font-size: 0.8rem;
                            font-weight: 600;
                        ">{tipo_absorcion}</span>
                        <p style="margin-top: 0.8rem; opacity: 0.8; font-size: 0.9rem; line-height: 1.6;">
                            <strong><span class="material-symbols-rounded" style="vertical-align: text-bottom; font-size: 1.2em;">bar_chart</span> Cafeína:</strong> {producto['mg_min']}-{producto['mg_max']} mg por porción<br>
                            <strong><span class="material-symbols-rounded" style="vertical-align: text-bottom; font-size: 1.2em;">medication</span> Dosis:</strong> {producto['dosis_recomendada']}<br>
                            <strong><span class="material-symbols-rounded" style="vertical-align: text-bottom; font-size: 1.2em;">attach_money</span> Costo:</strong> {producto['costo']}
                        </p>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                            <strong><span class="material-symbols-rounded" style="vertical-align: text-bottom; font-size: 1.2em;">check_circle</span> Indicado para:</strong> {producto['indicado']}<br>
                            <strong><span class="material-symbols-rounded" style="vertical-align: text-bottom; font-size: 1.2em;">warning</span> No recomendado:</strong> {producto['contraindicado']}<br>
                            <strong><span class="material-symbols-rounded" style="vertical-align: text-bottom; font-size: 1.2em;">emoji_events</span> Deportes:</strong> {', '.join(producto['deportes'])}
                        </p>
                        <p style="font-size: 0.8rem; opacity: 0.5; margin-top: 0.5rem;">
                            <strong>Marcas:</strong> {', '.join(producto['marcas'][:4])}{'...' if len(producto['marcas']) > 4 else ''}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================================================================
    # CÁLCULOS
    # ================================================================
    # Solución analítica (línea suave)
    t_analitico = np.linspace(0, duracion, 500)
    c_analitico = caffeine.solucion_analitica(t_analitico, dosis, ka, ke, peso)

    # Solución numérica (Euler)
    f_euler = partial(caffeine.ode_func, D0=dosis, ka=ka, ke=ke, peso_kg=peso)
    t_euler, c_euler = euler_method(f_euler, y0=0.0, t_start=0.0, t_end=duracion, dt=dt)

    # Analítica en los mismos puntos que Euler (para error)
    c_analitico_euler_pts = caffeine.solucion_analitica(t_euler, dosis, ka, ke, peso)

    # Métricas
    t_max = caffeine.tiempo_pico(ka, ke)
    c_max = caffeine.concentracion_pico(dosis, ka, ke, peso)
    bajon = caffeine.detectar_bajon(t_analitico, c_analitico)

    # ================================================================
    # RESULTADOS — ¿Qué significa para ti?
    # ================================================================
    st.markdown("---")
    st.subheader(":material/show_chart: Tu curva de cafeína")

    # Métricas principales (lenguaje humano)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        horas_pico = int(t_max)
        minutos_pico = int((t_max - horas_pico) * 60)
        st.metric(":material/bolt: Pico de energía", f"{horas_pico}h {minutos_pico}min")
    with col_m2:
        st.metric(":material/trending_up: Concentración máxima", f"{c_max:.2f} mg/L")
    with col_m3:
        st.metric(":material/hourglass_empty: Vida media", f"{vida_media:.1f} horas")
    with col_m4:
        if bajon:
            horas_bajon = int(bajon['t_bajon'])
            minutos_bajon = int((bajon['t_bajon'] - horas_bajon) * 60)
            st.metric(":material/bedtime: Bajón de energía", f"{horas_bajon}h {minutos_bajon}min")
        else:
            st.metric(":material/bedtime: Bajón de energía", "N/A")

    # Interpretación en lenguaje natural
    if bajon:
        producto_texto = f" de **{producto['nombre']}**" if producto else ""
        st.info(
            f":material/local_cafe: Con **{dosis} mg** de cafeína{producto_texto}, sentirás el **máximo efecto a los "
            f"{horas_pico}h {minutos_pico}min**. El efecto disminuirá al 50% aproximadamente "
            f"a las **{horas_bajon}h {minutos_bajon}min** después de consumirla. "
            f"Tu cuerpo tarda unas **{vida_media:.0f} horas** en eliminar la mitad de la cafeína."
        )

    # ================================================================
    # GRÁFICA PLOTLY
    # ================================================================
    titulo_grafica = f"Concentración de Cafeína en Sangre — {dosis} mg, {peso} kg"
    if producto:
        titulo_grafica = f"{producto['nombre']} ({dosis} mg) — {peso} kg"

    is_dark = st.session_state.get('dark_mode_active', False)
    color_linea = "#10B981" if is_dark else "#7c3aed"
    color_euler = "#0EA5E9" if is_dark else "#f59e0b"
    color_pico = "#0EA5E9" if is_dark else "#4ecdc4"
    color_bajon = "#F43F5E" if is_dark else "#ef4444"

    fig = go.Figure()

    # Solución analítica (línea continua)
    fig.add_trace(go.Scatter(
        x=t_analitico, y=c_analitico,
        mode='lines',
        name='Concentración real (solución exacta)',
        line=dict(color=color_linea, width=3),
        hovertemplate='<b>Hora %{x:.1f}</b><br>Concentración: %{y:.3f} mg/L<extra></extra>'
    ))

    # Solución Euler (puntos)
    fig.add_trace(go.Scatter(
        x=t_euler, y=c_euler,
        mode='markers',
        name=f'Aproximación numérica (Euler, dt={dt})',
        marker=dict(color=color_euler, size=4, symbol='circle', opacity=0.7),
        hovertemplate='<b>Hora %{x:.1f}</b><br>Euler: %{y:.3f} mg/L<extra></extra>'
    ))

    # Línea del pico
    fig.add_vline(
        x=t_max, line_dash="dot", line_color=color_pico,
        annotation_text=f"Pico: {t_max:.1f}h",
        annotation_position="top right",
        annotation_font=dict(color=color_pico, size=12)
    )

    # Línea del bajón (si existe)
    if bajon:
        fig.add_vline(
            x=bajon['t_bajon'], line_dash="dash", line_color=color_bajon,
            annotation_text=f"Bajón: {bajon['t_bajon']:.1f}h",
            annotation_position="top left",
            annotation_font=dict(color=color_bajon, size=12)
        )
        fig.add_hline(
            y=bajon['umbral'], line_dash="dot", line_color=color_bajon,
            opacity=0.3,
            annotation_text="20% del pico",
            annotation_position="bottom right",
            annotation_font=dict(color=color_bajon, size=10)
        )

    layout_kwargs = dict(
        title=titulo_grafica,
        xaxis_title="Tiempo (horas)",
        yaxis_title="Concentración en sangre (mg/L)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    if is_dark:
        layout_kwargs.update(dict(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8")
        ))
        
    fig.update_layout(**layout_kwargs)

    st.plotly_chart(fig, use_container_width=True)

    # ================================================================
    # PANEL PRO — Proceso matemático detallado
    # ================================================================
    st.markdown("---")

    with st.expander(":material/science: **Modo Pro** — Proceso matemático completo (Laplace, EDO, errores)", expanded=False):

        st.markdown(
            """
            <div class="pro-panel">
                <p style="opacity: 0.7; font-size: 0.85rem;">
                    Esta sección muestra el desarrollo matemático completo, ideal para
                    profesores, estudiantes de ingeniería y profesionales que deseen
                    entender el fundamento teórico del modelo.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Modelado matemático ---
        st.markdown("#### :material/architecture: Sistema de Ecuaciones Diferenciales")

        col_eq1, col_eq2 = st.columns(2)
        with col_eq1:
            st.markdown("**Ecuaciones del modelo:**")
            st.latex(r"\frac{dD}{dt} = -k_a \cdot D(t) \quad \text{(Absorción desde TGI)}")
            st.latex(r"\frac{dC}{dt} = \frac{k_a \cdot D(t)}{V_d} - k_e \cdot C(t) \quad \text{(Concentración en sangre)}")

        with col_eq2:
            st.markdown("**Condiciones iniciales:**")
            st.latex(rf"D(0) = D_0 = {dosis} \text{{ mg}}")
            st.latex(r"C(0) = 0 \text{ mg/L}")
            st.markdown("**Parámetros:**")
            st.latex(rf"k_a = {ka} \text{{ h}}^{{-1}}, \quad k_e = {ke:.3f} \text{{ h}}^{{-1}}")

        if producto:
            st.caption(
                f":material/lightbulb: **Nota:** El valor de k_a fue ajustado automáticamente a {ka:.2f} "
                f"basado en la velocidad de absorción de **{producto['nombre']}** "
                f"(factor ×{producto['ka_factor']})."
            )

        # --- Resolución por Laplace ---
        st.markdown("---")
        st.markdown("#### :material/sync: Resolución por Transformada de Laplace")

        with st.spinner("Calculando resolución simbólica con SymPy..."):
            try:
                laplace_result = caffeine.resolver_laplace_simbolico()

                st.markdown("**Paso 1 — Ecuación Diferencial Original:**")
                st.latex(laplace_result['ode_latex'])

                st.markdown(
                    "**Paso 2 — Aplicar Transformada de Laplace** "
                    "($\\mathcal{L}\\{f'(t)\\} = sF(s) - f(0)$, "
                    "$\\mathcal{L}\\{e^{-at}\\} = \\frac{1}{s+a}$):"
                )
                st.latex(laplace_result['laplace_ambos_lados'])

                st.markdown("**Paso 3 — Despejar $C(s)$:**")
                st.latex(r"C(s) = " + laplace_result['C_s_latex'])

                st.markdown("**Paso 4 — Transformada Inversa** ($\\mathcal{L}^{-1}$):")
                st.latex(r"C(t) = " + laplace_result['solucion_latex'])

                st.success(":material/check_circle: **Ecuación de Bateman** — Solución analítica exacta.")

            except Exception as e:
                st.warning(f"Error en resolución simbólica: {e}")
                st.latex(
                    r"C(t) = \frac{k_a \cdot D_0}{(k_a - k_e) \cdot V_d} "
                    r"\left( e^{-k_e t} - e^{-k_a t} \right)"
                )

        # --- Tabla de errores numéricos ---
        st.markdown("---")
        st.markdown("#### :material/table_chart: Error Numérico: Euler vs Solución Analítica")

        errores = calcular_errores(c_euler, c_analitico_euler_pts)

        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            st.metric("Error Abs. Promedio", f"{errores['error_abs_promedio']:.6f} mg/L")
        with col_e2:
            st.metric("Error Abs. Máximo", f"{errores['error_abs_maximo']:.6f} mg/L")
        with col_e3:
            st.metric("Error Rel. Promedio", f"{errores['error_rel_promedio']:.4f} %")

        step_display = max(1, len(t_euler) // 25)

        df_errores = pd.DataFrame({
            't (horas)': t_euler[::step_display],
            'C_euler (mg/L)': c_euler[::step_display],
            'C_analítica (mg/L)': c_analitico_euler_pts[::step_display],
            'Error Abs (mg/L)': errores['error_absoluto'][::step_display],
            'Error Rel (%)': errores['error_porcentual'][::step_display],
        })

        st.table(
            df_errores.style.format({
                't (horas)': '{:.2f}',
                'C_euler (mg/L)': '{:.6f}',
                'C_analítica (mg/L)': '{:.6f}',
                'Error Abs (mg/L)': '{:.6f}',
                'Error Rel (%)': '{:.4f}',
            }).hide(axis="index")
        )

        st.markdown(
            "*:material/lightbulb: **Tip**: Reduce el valor de `dt` en los parámetros avanzados para ver "
            "cómo el error de Euler disminuye al usar pasos más pequeños.*"
        )
