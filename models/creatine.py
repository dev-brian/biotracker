"""
BioTracker — Modelo de Saturación de Creatina
===============================================
Modela la acumulación de fosfocreatina (PCr) en el músculo esquelético
a lo largo de días/semanas de suplementación con monohidrato de creatina.

Ciencia:
    A diferencia de la cafeína, la creatina NO da energía instantánea.
    Funciona saturando las reservas intramusculares de fosfocreatina (PCr),
    que es el sustrato para regenerar ATP rápidamente durante esfuerzos
    explosivos (sistema fosfágeno, primeros 10 segundos de ejercicio intenso).

    El cuerpo degrada creatina a creatinina (producto de desecho) a una tasa
    constante de aproximadamente 1.7% diario, que se excreta por la orina.

Ecuación Diferencial:
    dS/dt = I - k * S(t)

    Donde:
        S(t) = nivel de fosfocreatina muscular (gramos)
        I = ingesta diaria de creatina (g/día)
        k = tasa de degradación diaria (≈ 0.017 día⁻¹, es decir ~1.7%/día)
        S(0) = S_0 (nivel inicial, típicamente 60-80% de saturación)

    Interpretación:
        - El término I (ingesta) INCREMENTA la fosfocreatina
        - El término k*S(t) (degradación) DISMINUYE la fosfocreatina
        - El equilibrio (estado estable) se alcanza cuando dS/dt = 0 → S_eq = I/k

Solución Analítica (via Transformada de Laplace):
    Aplicando Laplace a dS/dt = I - k*S(t) con S(0) = S_0:

    s*S(s) - S_0 = I/s - k*S(s)
    S(s)*(s + k) = I/s + S_0
    S(s) = I / (s*(s + k)) + S_0 / (s + k)

    Aplicando Laplace Inversa:
    S(t) = (I/k) * (1 - e^(-k*t)) + S_0 * e^(-k*t)
    S(t) = I/k + (S_0 - I/k) * e^(-k*t)

Fases de suplementación:
    - Fase de Carga: 20 g/día durante 5-7 días → saturación rápida
    - Fase de Mantenimiento: 3-5 g/día → mantiene la saturación
    - Sin suplementación: ~2 g/día (dieta normal) → saturación parcial (~60-80%)

Parámetros por defecto:
    k = 0.017 día⁻¹ (degradación ~1.7%/día)
    S_max = 160 g (capacidad máxima de PCr para ~70 kg de masa muscular)
    S_0 = 120 g (≈ 75% de saturación sin suplementación)

Referencias:
    - Hultman et al., 1996. Journal of Applied Physiology.
    - Kreider et al., 2017. Journal of the ISSN (Position Stand on Creatine).
"""

import numpy as np
import sympy as sp


# ============================================================================
# CONSTANTES DEL MODELO
# ============================================================================

# Tasa de degradación de creatina a creatinina (día⁻¹)
# Aproximadamente 1.7% del pool total se degrada diariamente
K_DEFAULT = 0.017

# Capacidad máxima de fosfocreatina muscular (gramos)
# Para un individuo de ~70 kg con ~30 kg de masa muscular
S_MAX_DEFAULT = 160.0

# Nivel inicial típico sin suplementación (gramos)
# Corresponde a ~75% de saturación (dieta omnívora normal)
S0_DEFAULT = 120.0

# Ingesta diaria por dieta normal (gramos/día)
# Sin suplementación, la dieta aporta ~1-2 g/día de creatina
I_DIETA_NORMAL = 2.0

# Fases de suplementación predefinidas
FASES = {
    'Fase de Carga': {'ingesta': 20.0, 'descripcion': '20 g/día durante 5-7 días'},
    'Fase de Mantenimiento': {'ingesta': 5.0, 'descripcion': '3-5 g/día indefinidamente'},
    'Sin Suplementación': {'ingesta': I_DIETA_NORMAL, 'descripcion': '~2 g/día (solo dieta)'},
}


# ============================================================================
# SOLUCIÓN ANALÍTICA
# ============================================================================

def solucion_analitica(t, I, k=K_DEFAULT, S0=S0_DEFAULT):
    """
    Calcula el nivel de fosfocreatina muscular usando la solución exacta.

    S(t) = I/k + (S_0 - I/k) * e^(-k*t)

    Parámetros:
        t (float o np.ndarray): Tiempo en días.
        I (float): Ingesta diaria de creatina (g/día).
        k (float): Tasa de degradación (día⁻¹).
        S0 (float): Nivel inicial de fosfocreatina (g).

    Retorna:
        S(t) (float o np.ndarray): Nivel de fosfocreatina en gramos.
    """
    S_eq = I / k  # Estado estable teórico
    return S_eq + (S0 - S_eq) * np.exp(-k * t)


def estado_estable(I, k=K_DEFAULT):
    """
    Calcula el nivel de saturación en estado estable (equilibrio).

    Cuando dS/dt = 0: S_eq = I / k

    Retorna:
        S_eq (float): Nivel de equilibrio en gramos.
    """
    return I / k


def dias_para_saturacion(I, k=K_DEFAULT, S0=S0_DEFAULT, S_max=S_MAX_DEFAULT, pct=0.95):
    """
    Calcula cuántos días tarda en alcanzar un porcentaje dado de saturación.

    Resolviendo S(t) = pct * S_max:
        t = -ln((pct*S_max - I/k) / (S_0 - I/k)) / k

    Parámetros:
        pct (float): Porcentaje de saturación objetivo (default 95%).

    Retorna:
        t_sat (float): Días para alcanzar la saturación objetivo, o None si no es alcanzable.
    """
    S_eq = I / k
    S_target = pct * S_max

    # Si el estado estable es menor que el objetivo, nunca se alcanza
    if S_eq < S_target and S0 < S_target:
        # Verificar si la curva alguna vez alcanza S_target
        if S_eq < S_target:
            return None

    # Si ya estamos por encima del objetivo
    if S0 >= S_target:
        return 0.0

    try:
        ratio = (S_target - S_eq) / (S0 - S_eq)
        if ratio <= 0:
            return None
        t_sat = -np.log(ratio) / k
        return float(t_sat) if t_sat > 0 else None
    except (ValueError, ZeroDivisionError):
        return None


def porcentaje_saturacion(S, S_max=S_MAX_DEFAULT):
    """
    Convierte gramos de fosfocreatina a porcentaje de saturación.

    Retorna:
        pct (float o np.ndarray): Porcentaje de saturación (0-100+).
    """
    return (S / S_max) * 100


# ============================================================================
# FUNCIÓN ODE PARA EL MÉTODO DE EULER
# ============================================================================

def ode_func(t, S, I, k=K_DEFAULT):
    """
    Define dS/dt para el método de Euler.

    dS/dt = I - k * S(t)

    Parámetros:
        t (float): Tiempo actual (no se usa explícitamente, pero requerido por el solver).
        S (float): Nivel actual de fosfocreatina.
        I (float): Ingesta diaria.
        k (float): Tasa de degradación.

    Retorna:
        dS/dt (float): Tasa de cambio del nivel de fosfocreatina.
    """
    return I - k * S


# ============================================================================
# RESOLUCIÓN SIMBÓLICA CON TRANSFORMADA DE LAPLACE (SymPy)
# ============================================================================

def resolver_laplace_simbolico():
    """
    Resuelve la EDO de creatina paso a paso usando la Transformada de Laplace.

    Proceso:
        1. EDO: dS/dt = I - k*S(t), S(0) = S_0
        2. Laplace: s*S(s) - S_0 = I/s - k*S(s)
        3. Despejar: S(s) = I/(s*(s+k)) + S_0/(s+k)
        4. Inversa: S(t) = I/k*(1 - e^(-kt)) + S_0*e^(-kt)

    Retorna:
        dict con expresiones LaTeX de cada paso.
    """
    # Símbolos
    t, s = sp.symbols('t s', positive=True)
    k, I_sym, S0 = sp.symbols('k I S_0', positive=True)
    S = sp.Function('S')

    # --- PASO 1: Definir la EDO ---
    ode = sp.Eq(S(t).diff(t), I_sym - k * S(t))
    ode_latex = sp.latex(ode)

    # --- PASO 2: Aplicar Transformada de Laplace ---
    S_s = sp.Symbol('S_s')  # S(s) como símbolo algebraico

    # L{dS/dt} = s*S(s) - S(0) = s*S(s) - S_0
    # L{I} = I/s
    # L{k*S(t)} = k*S(s)
    eq_laplace = sp.Eq(s * S_s - S0, I_sym / s - k * S_s)
    laplace_ambos_lados = sp.latex(eq_laplace).replace('S_{s}', 'S(s)')

    # --- PASO 3: Resolver para S(s) ---
    S_s_expr = sp.solve(eq_laplace, S_s)[0]
    S_s_latex = sp.latex(S_s_expr).replace('S_{s}', 'S(s)')

    # --- PASO 4: Transformada Inversa ---
    S_t_expr = sp.inverse_laplace_transform(S_s_expr, s, t)
    S_t_simplified = sp.simplify(S_t_expr)
    solucion_latex = sp.latex(S_t_simplified)

    return {
        'ode_latex': ode_latex,
        'laplace_ambos_lados': laplace_ambos_lados,
        'S_s_latex': S_s_latex,
        'solucion_latex': solucion_latex,
        'solucion_sympy': S_t_simplified,
    }
