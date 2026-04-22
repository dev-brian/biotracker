"""
BioTracker — Vista del Módulo de Cafeína
=========================================
Interfaz amigable para el modelo farmacocinético de cafeína.
Modo normal: gráficas y métricas comprensibles para todos.
Modo Pro: proceso de Laplace paso a paso + tabla de errores detallada.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from functools import partial

from models import caffeine
from models.solvers import euler_method, calcular_errores


def render():
    """Renderiza la página completa del módulo de cafeína."""

    st.header("☕ Cafeína — ¿Cuánto dura el efecto?")
    st.markdown(
        "Cuando tomas café, tu cuerpo **absorbe** la cafeína rápidamente y luego "
        "la **elimina** poco a poco. Esta simulación te muestra exactamente "
        "**cuándo sientes el pico de energía** y **cuándo llega el bajón**."
    )

    # ================================================================
    # SIDEBAR — Parámetros de entrada
    # ================================================================
    st.sidebar.markdown("### ☕ Tu consumo")

    dosis = st.sidebar.slider(
        "¿Cuánta cafeína consumiste? (mg)",
        min_value=50, max_value=400, value=200, step=25,
        help="☕ Café filtrado: ~95 mg · ☕ Espresso: ~63 mg · 🥤 Energy drink: ~80-160 mg · 💊 Pastilla: ~200 mg"
    )

    peso = st.sidebar.slider(
        "Tu peso corporal (kg)",
        min_value=40, max_value=120, value=70, step=5,
        help="Tu peso afecta qué tan concentrada queda la cafeína en tu sangre."
    )

    # Parámetros avanzados (colapsados por defecto)
    with st.sidebar.expander("⚙️ Parámetros avanzados"):
        ka = st.slider(
            "Velocidad de absorción (k_a)",
            min_value=1.0, max_value=8.0, value=caffeine.KA_DEFAULT, step=0.1,
            help="Qué tan rápido pasa la cafeína del estómago a la sangre. Mayor = más rápido."
        )

        ke = st.slider(
            "Velocidad de eliminación (k_e)",
            min_value=0.05, max_value=0.30, value=caffeine.KE_DEFAULT, step=0.001,
            format="%.3f",
            help="Qué tan rápido tu hígado procesa la cafeína. Varía por genética."
        )

        dt = st.slider(
            "Precisión de Euler (dt)",
            min_value=0.01, max_value=1.0, value=0.1, step=0.01,
            help="Tamaño del paso del método numérico. Menor = más preciso."
        )

        duracion = st.slider(
            "Horas a simular",
            min_value=6, max_value=48, value=24, step=1
        )

    # Usar defaults si no se abrió el expander
    if 'ka' not in dir():
        ka = caffeine.KA_DEFAULT
    if 'ke' not in dir():
        ke = caffeine.KE_DEFAULT
    if 'dt' not in dir():
        dt = 0.1
    if 'duracion' not in dir():
        duracion = 24

    vida_media = np.log(2) / ke

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
    st.subheader("📊 Tu curva de cafeína")

    # Métricas principales (lenguaje humano)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        # Convertir a formato hora:minutos legible
        horas_pico = int(t_max)
        minutos_pico = int((t_max - horas_pico) * 60)
        st.metric("⚡ Pico de energía", f"{horas_pico}h {minutos_pico}min")
    with col_m2:
        st.metric("📈 Concentración máxima", f"{c_max:.2f} mg/L")
    with col_m3:
        st.metric("⏳ Vida media", f"{vida_media:.1f} horas")
    with col_m4:
        if bajon:
            horas_bajon = int(bajon['t_bajon'])
            minutos_bajon = int((bajon['t_bajon'] - horas_bajon) * 60)
            st.metric("💤 Bajón de energía", f"{horas_bajon}h {minutos_bajon}min")
        else:
            st.metric("💤 Bajón de energía", "N/A")

    # Interpretación en lenguaje natural
    if bajon:
        hora_cafe = "por la mañana"
        st.info(
            f"☕ Con **{dosis} mg** de cafeína, sentirás el **máximo efecto a los "
            f"{horas_pico}h {minutos_pico}min**. El efecto disminuirá al 50% aproximadamente "
            f"a las **{horas_bajon}h {minutos_bajon}min** después de consumirla. "
            f"Tu cuerpo tarda unas **{vida_media:.0f} horas** en eliminar la mitad de la cafeína."
        )

    # ================================================================
    # GRÁFICA PLOTLY
    # ================================================================

    fig = go.Figure()

    # Solución analítica (línea continua)
    fig.add_trace(go.Scatter(
        x=t_analitico, y=c_analitico,
        mode='lines',
        name='Concentración real (solución exacta)',
        line=dict(color='#7c3aed', width=3),
        hovertemplate='<b>Hora %{x:.1f}</b><br>Concentración: %{y:.3f} mg/L<extra></extra>'
    ))

    # Solución Euler (puntos)
    fig.add_trace(go.Scatter(
        x=t_euler, y=c_euler,
        mode='markers',
        name=f'Aproximación numérica (Euler, dt={dt})',
        marker=dict(color='#f59e0b', size=4, symbol='circle', opacity=0.7),
        hovertemplate='<b>Hora %{x:.1f}</b><br>Euler: %{y:.3f} mg/L<extra></extra>'
    ))

    # Línea del pico
    fig.add_vline(
        x=t_max, line_dash="dot", line_color="#4ecdc4",
        annotation_text=f"⚡ Pico: {t_max:.1f}h",
        annotation_position="top right",
        annotation_font=dict(color="#4ecdc4", size=12)
    )

    # Línea del bajón (si existe)
    if bajon:
        fig.add_vline(
            x=bajon['t_bajon'], line_dash="dash", line_color="#ef4444",
            annotation_text=f"💤 Bajón: {bajon['t_bajon']:.1f}h",
            annotation_position="top left",
            annotation_font=dict(color="#ef4444", size=12)
        )
        fig.add_hline(
            y=bajon['umbral'], line_dash="dot", line_color="#ef4444",
            opacity=0.3,
            annotation_text="50% del pico",
            annotation_position="bottom right",
            annotation_font=dict(color="#ef4444", size=10)
        )

    fig.update_layout(
        title=dict(
            text=f"Concentración de Cafeína en Sangre — {dosis} mg, {peso} kg",
            font=dict(size=15)
        ),
        xaxis_title="Tiempo después de consumir (horas)",
        yaxis_title="Concentración en sangre (mg/L)",
        template="plotly_dark",
        height=480,
        legend=dict(
            yanchor="top", y=0.99,
            xanchor="right", x=0.99,
            bgcolor="rgba(0,0,0,0.5)",
            font=dict(size=11)
        ),
        hovermode="x unified",
        margin=dict(t=50, b=50),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ================================================================
    # PANEL PRO — Proceso matemático detallado
    # ================================================================
    st.markdown("---")

    with st.expander("🔬 **Modo Pro** — Proceso matemático completo (Laplace, EDO, errores)", expanded=False):

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
        st.markdown("#### 📐 Sistema de Ecuaciones Diferenciales")

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

        # --- Resolución por Laplace ---
        st.markdown("---")
        st.markdown("#### 🔄 Resolución por Transformada de Laplace")

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

                st.success("✅ **Ecuación de Bateman** — Solución analítica exacta.")

            except Exception as e:
                st.warning(f"Error en resolución simbólica: {e}")
                st.latex(
                    r"C(t) = \frac{k_a \cdot D_0}{(k_a - k_e) \cdot V_d} "
                    r"\left( e^{-k_e t} - e^{-k_a t} \right)"
                )

        # --- Tabla de errores numéricos ---
        st.markdown("---")
        st.markdown("#### 📋 Error Numérico: Euler vs Solución Analítica")

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

        st.dataframe(
            df_errores.style.format({
                't (horas)': '{:.2f}',
                'C_euler (mg/L)': '{:.6f}',
                'C_analítica (mg/L)': '{:.6f}',
                'Error Abs (mg/L)': '{:.6f}',
                'Error Rel (%)': '{:.4f}',
            }),
            use_container_width=True,
            hide_index=True,
            height=400,
        )

        st.markdown(
            "*💡 **Tip**: Reduce el valor de `dt` en los parámetros avanzados para ver "
            "cómo el error de Euler disminuye al usar pasos más pequeños.*"
        )
