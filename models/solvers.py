"""
BioTracker — Métodos Numéricos (Solver Genérico)
=================================================
Implementación del Método de Euler para resolver Ecuaciones Diferenciales Ordinarias (EDOs).

El Método de Euler es una aproximación numérica de primer orden que discretiza la solución
de una EDO dy/dt = f(t, y) usando la fórmula iterativa:
    y_{n+1} = y_n + dt * f(t_n, y_n)

donde dt es el tamaño del paso (step size).
"""

import numpy as np


def euler_method(f, y0, t_start, t_end, dt):
    """
    Resuelve una EDO dy/dt = f(t, y) usando el Método de Euler.

    Parámetros:
        f (callable): Función f(t, y) que define la derivada dy/dt.
        y0 (float): Condición inicial y(t_start) = y0.
        t_start (float): Tiempo inicial de la simulación.
        t_end (float): Tiempo final de la simulación.
        dt (float): Tamaño del paso temporal (step size).

    Retorna:
        t_vals (np.ndarray): Array de puntos temporales [t_start, t_start+dt, ..., t_end].
        y_vals (np.ndarray): Array de valores aproximados de y en cada punto temporal.

    Ejemplo:
        >>> # Resolver dy/dt = -0.5*y, y(0) = 10
        >>> f = lambda t, y: -0.5 * y
        >>> t, y = euler_method(f, y0=10, t_start=0, t_end=10, dt=0.1)
    """
    # Número de pasos
    n_steps = int(np.ceil((t_end - t_start) / dt))

    # Inicializar arrays
    t_vals = np.zeros(n_steps + 1)
    y_vals = np.zeros(n_steps + 1)

    # Condiciones iniciales
    t_vals[0] = t_start
    y_vals[0] = y0

    # Iteración de Euler: y_{n+1} = y_n + dt * f(t_n, y_n)
    for i in range(n_steps):
        y_vals[i + 1] = y_vals[i] + dt * f(t_vals[i], y_vals[i])
        t_vals[i + 1] = t_vals[i] + dt

    return t_vals, y_vals


def calcular_errores(y_numerico, y_analitico):
    """
    Calcula los errores entre la solución numérica (Euler) y la solución analítica (Laplace).

    Parámetros:
        y_numerico (np.ndarray): Valores de la solución numérica (Euler).
        y_analitico (np.ndarray): Valores de la solución analítica exacta.

    Retorna:
        dict con:
            - error_absoluto (np.ndarray): |y_analitico - y_numerico|
            - error_relativo (np.ndarray): |error_absoluto / y_analitico| (0 donde y_analitico=0)
            - error_porcentual (np.ndarray): error_relativo * 100
            - error_abs_promedio (float): Promedio del error absoluto
            - error_abs_maximo (float): Máximo error absoluto
            - error_rel_promedio (float): Promedio del error relativo porcentual
    """
    error_absoluto = np.abs(y_analitico - y_numerico)

    # Evitar división por cero: donde y_analitico es ~0, error relativo = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        error_relativo = np.where(
            np.abs(y_analitico) > 1e-10,
            error_absoluto / np.abs(y_analitico),
            0.0
        )

    error_porcentual = error_relativo * 100

    return {
        'error_absoluto': error_absoluto,
        'error_relativo': error_relativo,
        'error_porcentual': error_porcentual,
        'error_abs_promedio': float(np.mean(error_absoluto)),
        'error_abs_maximo': float(np.max(error_absoluto)),
        'error_rel_promedio': float(np.mean(error_porcentual)),
    }
