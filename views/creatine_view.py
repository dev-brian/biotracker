"""
BioTracker — Vista del Módulo de Creatina
==========================================
Interfaz amigable para el modelo de saturación de creatina muscular.
Modo normal: gráficas y métricas comprensibles para todos.
Modo Pro: proceso de Laplace + tabla de errores detallada.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from functools import partial

from models import creatine
from models.solvers import euler_method, calcular_errores


def render():
    """Renderiza la página completa del módulo de creatina."""

    st.header("💪 Creatina — ¿Cuántos días para ver resultados?")
    st.markdown(
        "La creatina **no da energía instantánea** como la cafeína. Funciona **acumulándose** "
        "en tus músculos día tras día, hasta que alcanzas la saturación máxima. "
        "Esta simulación te muestra **cuántos días necesitas** según tu dosis."
    )

    # ================================================================
    # SIDEBAR — Parámetros de entrada
    # ================================================================
    st.sidebar.markdown("### 💪 Tu suplementación")

    fase = st.sidebar.radio(
        "¿Qué fase estás siguiendo?",
        list(creatine.FASES.keys()),
        help="🏃 Carga: saturación rápida (5-7 días). 🚶 Mantenimiento: sostener el nivel a largo plazo."
    )

    st.sidebar.caption(f"📋 {creatine.FASES[fase]['descripcion']}")

    ingesta_default = creatine.FASES[fase]['ingesta']
    ingesta = st.sidebar.slider(
        "Gramos por día (g/día)",
        min_value=1.0, max_value=25.0, value=ingesta_default, step=0.5,
        help="Cantidad total de creatina que consumes diariamente (dieta + suplemento)."
    )

    # Parámetros avanzados (colapsados)
    with st.sidebar.expander("⚙️ Parámetros avanzados"):
        k = st.slider(
            "Tasa de degradación (k)",
            min_value=0.010, max_value=0.050, value=creatine.K_DEFAULT, step=0.001,
            format="%.3f",
            help="Tu cuerpo degrada ~1.7% de la creatina muscular cada día, convirtiéndola en creatinina."
        )

        S_max = st.slider(
            "Capacidad máxima muscular (g)",
            min_value=100.0, max_value=200.0, value=creatine.S_MAX_DEFAULT, step=5.0,
            help="Depende de tu masa muscular. Más músculo = más capacidad de almacenar PCr."
        )

        S0_pct = st.slider(
            "Saturación inicial (%)",
            min_value=30, max_value=100, value=75, step=5,
            help="Sin suplementación, normalmente tienes 60-80% de saturación."
        )

        duracion = st.slider(
            "Días a simular",
            min_value=7, max_value=90, value=30, step=1
        )

        dt = st.slider(
            "Precisión de Euler (dt en días)",
            min_value=0.1, max_value=2.0, value=0.5, step=0.1,
            help="Tamaño del paso del método numérico."
        )

    # Defaults si no se abrió expander
    if 'k' not in dir():
        k = creatine.K_DEFAULT
    if 'S_max' not in dir():
        S_max = creatine.S_MAX_DEFAULT
    if 'S0_pct' not in dir():
        S0_pct = 75
    if 'duracion' not in dir():
        duracion = 30
    if 'dt' not in dir():
        dt = 0.5

    S0 = S_max * (S0_pct / 100)

    # ================================================================
    # CÁLCULOS
    # ================================================================
    # Solución analítica
    t_analitico = np.linspace(0, duracion, 500)
    s_analitico = creatine.solucion_analitica(t_analitico, ingesta, k, S0)
    s_analitico_pct = creatine.porcentaje_saturacion(s_analitico, S_max)

    # Solución numérica (Euler)
    f_euler = partial(creatine.ode_func, I=ingesta, k=k)
    t_euler, s_euler = euler_method(f_euler, y0=S0, t_start=0.0, t_end=duracion, dt=dt)
    s_euler_pct = creatine.porcentaje_saturacion(s_euler, S_max)

    # Analítica en puntos de Euler
    s_analitico_euler_pts = creatine.solucion_analitica(t_euler, ingesta, k, S0)

    # Métricas
    S_eq = creatine.estado_estable(ingesta, k)
    S_eq_pct = creatine.porcentaje_saturacion(S_eq, S_max)
    dias_sat = creatine.dias_para_saturacion(ingesta, k, S0, S_max, pct=0.95)

    # ================================================================
    # RESULTADOS — ¿Qué significa para ti?
    # ================================================================
    st.markdown("---")
    st.subheader("📊 Tu curva de saturación")

    # Métricas principales
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("📦 Nivel inicial", f"{S0_pct}%")
    with col_m2:
        nivel_final = min(S_eq_pct, 100 * (S_eq / S_max))
        st.metric("🎯 Nivel de equilibrio", f"{nivel_final:.0f}%")
    with col_m3:
        if dias_sat is not None and dias_sat <= duracion:
            st.metric("📅 Días para 95%", f"{dias_sat:.0f} días")
        else:
            st.metric("📅 Días para 95%", "No alcanzable ⚠️")
    with col_m4:
        st.metric("📉 Degradación diaria", f"{k*100:.1f}%")

    # Interpretación en lenguaje natural
    if dias_sat is not None and dias_sat <= duracion:
        st.info(
            f"💪 Con **{ingesta} g/día** ({fase.lower()}), tus músculos alcanzarán el "
            f"**95% de saturación en ~{dias_sat:.0f} días**. Tu nivel de equilibrio final "
            f"será de **{S_eq:.0f} g** ({nivel_final:.0f}% de tu capacidad). "
            f"Tu cuerpo degrada un **{k*100:.1f}%** de la creatina almacenada cada día."
        )
    elif S_eq_pct > 100:
        st.info(
            f"💪 Con **{ingesta} g/día**, superarás la capacidad máxima estimada. "
            f"En la práctica, el cuerpo excreta el exceso por orina."
        )
    else:
        st.warning(
            f"⚠️ Con **{ingesta} g/día**, tu nivel de equilibrio será de **{nivel_final:.0f}%**. "
            f"Considera aumentar la dosis para alcanzar saturación completa."
        )

    # ================================================================
    # GRÁFICA PLOTLY
    # ================================================================

    fig = go.Figure()

    # Solución analítica
    fig.add_trace(go.Scatter(
        x=t_analitico, y=s_analitico_pct,
        mode='lines',
        name='Saturación real (solución exacta)',
        line=dict(color='#4ecdc4', width=3),
        hovertemplate='<b>Día %{x:.0f}</b><br>Saturación: %{y:.1f}%<extra></extra>'
    ))

    # Método de Euler
    fig.add_trace(go.Scatter(
        x=t_euler, y=s_euler_pct,
        mode='markers',
        name=f'Aproximación numérica (Euler, dt={dt})',
        marker=dict(color='#f59e0b', size=5, symbol='circle', opacity=0.7),
        hovertemplate='<b>Día %{x:.0f}</b><br>Euler: %{y:.1f}%<extra></extra>'
    ))

    # Línea de 95% saturación
    fig.add_hline(
        y=95.0, line_dash="dot", line_color="#a78bfa",
        annotation_text="95% saturación",
        annotation_position="bottom right",
        annotation_font=dict(color="#a78bfa", size=11)
    )

    # Línea de 100% capacidad
    fig.add_hline(
        y=100.0, line_dash="solid", line_color="#7c3aed",
        opacity=0.4,
        annotation_text="100% capacidad",
        annotation_position="top right",
        annotation_font=dict(color="#7c3aed", size=11)
    )

    # Anotación de día de saturación
    if dias_sat is not None and dias_sat <= duracion:
        fig.add_vline(
            x=dias_sat, line_dash="dash", line_color="#4ecdc4",
            annotation_text=f"📅 Día {dias_sat:.0f}",
            annotation_position="top left",
            annotation_font=dict(color="#4ecdc4", size=12)
        )

    fig.update_layout(
        title=dict(
            text=f"Saturación de Fosfocreatina — {fase}: {ingesta} g/día",
            font=dict(size=15)
        ),
        xaxis_title="Días de suplementación",
        yaxis_title="Saturación muscular (%)",
        template="plotly_dark",
        height=480,
        legend=dict(
            yanchor="bottom", y=0.01,
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
                    Desarrollo matemático del modelo de saturación de creatina.
                    Incluye la ecuación diferencial, resolución por Laplace, y
                    análisis del error numérico.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Modelado matemático ---
        st.markdown("#### 📐 Ecuación Diferencial del Modelo")

        col_eq1, col_eq2 = st.columns(2)
        with col_eq1:
            st.latex(r"\frac{dS}{dt} = I - k \cdot S(t)")
            st.markdown(
                "- $S(t)$ = fosfocreatina muscular (g)\n"
                "- $I$ = ingesta diaria (g/día)\n"
                "- $k$ = tasa de degradación (día⁻¹)"
            )

        with col_eq2:
            st.markdown("**Condiciones iniciales:**")
            st.latex(rf"S(0) = {S0:.1f} \text{{ g}} \quad ({S0_pct}\%)")
            st.latex(rf"I = {ingesta} \text{{ g/día}}, \quad k = {k:.3f}")
            st.latex(rf"S_{{eq}} = \frac{{I}}{{k}} = {S_eq:.1f} \text{{ g}}")

        # --- Resolución por Laplace ---
        st.markdown("---")
        st.markdown("#### 🔄 Resolución por Transformada de Laplace")

        with st.spinner("Calculando resolución simbólica..."):
            try:
                laplace_result = creatine.resolver_laplace_simbolico()

                st.markdown("**Paso 1 — EDO original:**")
                st.latex(laplace_result['ode_latex'])

                st.markdown(
                    "**Paso 2 — Transformada de Laplace** "
                    "($\\mathcal{L}\\{f'(t)\\} = sF(s) - f(0)$, "
                    "$\\mathcal{L}\\{1\\} = \\frac{1}{s}$):"
                )
                st.latex(laplace_result['laplace_ambos_lados'])

                st.markdown("**Paso 3 — Despejar $S(s)$:**")
                st.latex(r"S(s) = " + laplace_result['S_s_latex'])

                st.markdown("**Paso 4 — Transformada Inversa:**")
                st.latex(r"S(t) = " + laplace_result['solucion_latex'])

                st.success("✅ Solución analítica exacta obtenida por Laplace.")

            except Exception as e:
                st.warning(f"Error en resolución simbólica: {e}")
                st.latex(r"S(t) = \frac{I}{k} + \left(S_0 - \frac{I}{k}\right) e^{-kt}")

        # --- Tabla de errores ---
        st.markdown("---")
        st.markdown("#### 📋 Error Numérico: Euler vs Analítica")

        errores = calcular_errores(s_euler, s_analitico_euler_pts)

        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            st.metric("Error Abs. Promedio", f"{errores['error_abs_promedio']:.4f} g")
        with col_e2:
            st.metric("Error Abs. Máximo", f"{errores['error_abs_maximo']:.4f} g")
        with col_e3:
            st.metric("Error Rel. Promedio", f"{errores['error_rel_promedio']:.4f} %")

        step_display = max(1, len(t_euler) // 25)

        df_errores = pd.DataFrame({
            't (días)': t_euler[::step_display],
            'S_euler (g)': s_euler[::step_display],
            'S_analítica (g)': s_analitico_euler_pts[::step_display],
            'Saturación (%)': s_euler_pct[::step_display],
            'Error Abs (g)': errores['error_absoluto'][::step_display],
            'Error Rel (%)': errores['error_porcentual'][::step_display],
        })

        st.dataframe(
            df_errores.style.format({
                't (días)': '{:.1f}',
                'S_euler (g)': '{:.2f}',
                'S_analítica (g)': '{:.2f}',
                'Saturación (%)': '{:.1f}',
                'Error Abs (g)': '{:.4f}',
                'Error Rel (%)': '{:.4f}',
            }),
            use_container_width=True,
            hide_index=True,
            height=400,
        )

        st.markdown(
            "*💡 **Tip**: La creatina tiene cambios lentos (días), así que Euler es muy preciso "
            "incluso con pasos grandes. Compáralo con la cafeína donde el error es mayor.*"
        )
