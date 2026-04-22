"""
BioTracker — Modelo Farmacocinético de Cafeína
================================================
Modela la absorción y eliminación de cafeína en el cuerpo humano
usando un modelo de UN compartimento con absorción oral.

Ciencia:
    La cafeína antagoniza los receptores de adenosina en el cerebro,
    promoviendo el estado de alerta. Se absorbe rápidamente en el
    tracto gastrointestinal (TGI) y se elimina por metabolismo hepático
    (enzima CYP1A2).

Sistema de Ecuaciones Diferenciales:
    Sea D(t) la cantidad de cafeína en el TGI y C(t) la concentración en sangre:

    dD/dt = -k_a * D(t)                    ... (1) Absorción desde el TGI
    dC/dt = k_a * D(t) - k_e * C(t)        ... (2) Cambio en concentración sanguínea

    Donde:
        k_a = constante de absorción (rapidez de paso del TGI a la sangre)
        k_e = constante de eliminación (rapidez del metabolismo hepático)
        D(0) = D_0 (dosis administrada)
        C(0) = 0 (no hay cafeína en sangre al inicio)

Solución Analítica (Ecuación de Bateman):
    Resolviendo (1): D(t) = D_0 * e^(-k_a * t)
    Sustituyendo en (2) y resolviendo via Transformada de Laplace:

    C(t) = (k_a * D_0) / (k_a - k_e) * (e^(-k_e * t) - e^(-k_a * t))

    Esta es la Ecuación de Bateman, que describe el perfil farmacocinético
    clásico: un pico de concentración seguido de un declive exponencial.

Parámetros por defecto (valores fisiológicos reales):
    k_a = 4.0 h⁻¹  (absorción rápida, T_abs ≈ 10-15 min)
    k_e = 0.139 h⁻¹ (vida media ≈ 5 horas: t_1/2 = ln(2)/k_e)
"""

import numpy as np
import sympy as sp


# ============================================================================
# CONSTANTES FARMACOCINÉTICAS POR DEFECTO
# ============================================================================

# Constante de absorción gastrointestinal (h⁻¹)
# Referencia: Blanchard & Sawers, 1983. European Journal of Clinical Pharmacology.
KA_DEFAULT = 4.0

# Constante de eliminación hepática (h⁻¹)
# Vida media típica: ~5 horas → k_e = ln(2)/5 ≈ 0.139
# Referencia: Fredholm et al., 1999. Pharmacological Reviews.
KE_DEFAULT = 0.139

# Volumen de distribución aparente (L/kg)
# Referencia: Bonati et al., 1982. Clinical Pharmacokinetics.
VD_DEFAULT = 0.7


# ============================================================================
# SOLUCIÓN ANALÍTICA (Ecuación de Bateman)
# ============================================================================

def solucion_analitica(t, D0, ka=KA_DEFAULT, ke=KE_DEFAULT, peso_kg=70.0):
    """
    Calcula la concentración plasmática de cafeína usando la Ecuación de Bateman.

    C(t) = (k_a * D_0) / ((k_a - k_e) * V_d * peso) * (e^(-k_e*t) - e^(-k_a*t))

    Parámetros:
        t (float o np.ndarray): Tiempo en horas después de la ingesta.
        D0 (float): Dosis de cafeína en mg.
        ka (float): Constante de absorción (h⁻¹).
        ke (float): Constante de eliminación (h⁻¹).
        peso_kg (float): Peso corporal en kg.

    Retorna:
        C(t) (float o np.ndarray): Concentración plasmática en mg/L.
    """
    Vd = VD_DEFAULT * peso_kg  # Volumen de distribución total (L)
    coeficiente = (ka * D0) / ((ka - ke) * Vd)
    return coeficiente * (np.exp(-ke * t) - np.exp(-ka * t))


def tiempo_pico(ka=KA_DEFAULT, ke=KE_DEFAULT):
    """
    Calcula el tiempo exacto en que la concentración alcanza su máximo.

    Se obtiene igualando dC/dt = 0:
        t_max = ln(k_a / k_e) / (k_a - k_e)

    Retorna:
        t_max (float): Tiempo del pico en horas.
    """
    return np.log(ka / ke) / (ka - ke)


def concentracion_pico(D0, ka=KA_DEFAULT, ke=KE_DEFAULT, peso_kg=70.0):
    """
    Calcula la concentración máxima (C_max) alcanzada.

    Retorna:
        C_max (float): Concentración pico en mg/L.
    """
    t_max = tiempo_pico(ka, ke)
    return solucion_analitica(t_max, D0, ka, ke, peso_kg)


# ============================================================================
# FUNCIÓN ODE PARA EL MÉTODO DE EULER
# ============================================================================

def ode_func(t, C, D0, ka=KA_DEFAULT, ke=KE_DEFAULT, peso_kg=70.0):
    """
    Define dC/dt para el método de Euler.

    dC/dt = (k_a * D_0 * e^(-k_a*t)) / (V_d * peso) - k_e * C(t)

    Nota: D(t) = D_0 * e^(-k_a*t) ya está sustituido (solución de la ec. (1)).

    Parámetros:
        t (float): Tiempo actual.
        C (float): Concentración actual.
        D0, ka, ke, peso_kg: Parámetros del modelo.

    Retorna:
        dC/dt (float): Tasa de cambio de la concentración.
    """
    Vd = VD_DEFAULT * peso_kg
    absorcion = (ka * D0 * np.exp(-ka * t)) / Vd
    eliminacion = ke * C
    return absorcion - eliminacion


# ============================================================================
# DETECCIÓN DE "BAJÓN DE ENERGÍA"
# ============================================================================

def detectar_bajon(t_array, c_array, umbral_pct=0.50):
    """
    Detecta cuándo la concentración cae por debajo de un porcentaje del pico.

    Esto simula el "bajón de energía" que las personas experimentan
    cuando la cafeína baja del umbral de eficacia.

    Parámetros:
        t_array (np.ndarray): Array de tiempos.
        c_array (np.ndarray): Array de concentraciones.
        umbral_pct (float): Porcentaje del pico que define el "bajón" (default 50%).

    Retorna:
        dict con t_bajon, c_bajon, t_pico, c_pico, o None si no se detecta.
    """
    idx_pico = np.argmax(c_array)
    c_pico = c_array[idx_pico]
    t_pico = t_array[idx_pico]
    umbral = c_pico * umbral_pct

    # Buscar el primer cruce del umbral DESPUÉS del pico
    for i in range(idx_pico + 1, len(c_array)):
        if c_array[i] <= umbral:
            return {
                't_pico': float(t_pico),
                'c_pico': float(c_pico),
                't_bajon': float(t_array[i]),
                'c_bajon': float(c_array[i]),
                'umbral': float(umbral),
            }

    return None


# ============================================================================
# RESOLUCIÓN SIMBÓLICA CON TRANSFORMADA DE LAPLACE (SymPy)
# ============================================================================

def resolver_laplace_simbolico():
    """
    Resuelve la EDO de cafeína paso a paso usando la Transformada de Laplace
    con SymPy. Retorna las expresiones LaTeX de cada paso para mostrar en la UI.

    El proceso es:
        1. Definir la EDO: dC/dt + k_e*C = (k_a*D_0/V_d) * e^(-k_a*t)
        2. Aplicar Transformada de Laplace a ambos lados
        3. Resolver para C(s)
        4. Aplicar Transformada Inversa de Laplace
        5. Obtener C(t): la Ecuación de Bateman

    Retorna:
        dict con claves:
            - 'ode_latex': La EDO original en LaTeX
            - 'laplace_ambos_lados': La ecuación en el dominio de s
            - 'C_s_latex': C(s) despejada
            - 'solucion_latex': C(t) final (Bateman)
            - 'solucion_sympy': Expresión SymPy de C(t)
    """
    # Símbolos
    t, s = sp.symbols('t s', positive=True)
    ka, ke, D0, Vd = sp.symbols('k_a k_e D_0 V_d', positive=True)
    C = sp.Function('C')

    # --- PASO 1: Definir la EDO ---
    # El término fuente es la cafeína llegando del TGI: (ka * D0 / Vd) * exp(-ka*t)
    fuente = (ka * D0 / Vd) * sp.exp(-ka * t)
    ode = sp.Eq(C(t).diff(t), fuente - ke * C(t))
    ode_latex = sp.latex(ode)

    # --- PASO 2: Aplicar Transformada de Laplace ---
    # L{dC/dt} = s*C(s) - C(0), con C(0) = 0 → s*C(s)
    # L{k_e * C(t)} = k_e * C(s)
    # L{(ka*D0/Vd) * exp(-ka*t)} = (ka*D0/Vd) * 1/(s + ka)
    C_s = sp.Symbol('C_s')  # C(s) como símbolo algebraico

    lado_izq = s * C_s  # L{dC/dt} = s*C(s) - 0
    lado_der = (ka * D0 / Vd) / (s + ka) - ke * C_s

    eq_laplace = sp.Eq(lado_izq, lado_der)
    laplace_ambos_lados = sp.latex(eq_laplace).replace('C_{s}', 'C(s)')

    # --- PASO 3: Resolver para C(s) ---
    # s*C(s) + ke*C(s) = (ka*D0/Vd) / (s + ka)
    # C(s) * (s + ke) = (ka*D0/Vd) / (s + ka)
    # C(s) = (ka*D0/Vd) / ((s + ka)(s + ke))
    C_s_expr = sp.solve(eq_laplace, C_s)[0]
    C_s_latex = sp.latex(C_s_expr).replace('C_{s}', 'C(s)')

    # --- PASO 4: Transformada Inversa de Laplace ---
    # Usando fracciones parciales y la inversa:
    # L⁻¹{1/((s+a)(s+b))} = (e^(-bt) - e^(-at)) / (a - b)
    C_t_expr = sp.inverse_laplace_transform(C_s_expr, s, t)
    C_t_simplified = sp.simplify(C_t_expr)
    solucion_latex = sp.latex(C_t_simplified)

    return {
        'ode_latex': ode_latex,
        'laplace_ambos_lados': laplace_ambos_lados,
        'C_s_latex': C_s_latex,
        'solucion_latex': solucion_latex,
        'solucion_sympy': C_t_simplified,
    }
