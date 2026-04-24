# 📋 BioTracker — Estado del Proyecto

> **Última actualización:** 24 de abril de 2026  
> **Sprint:** Día 3 de 5  
> **Equipo:** Brian (desarrollo) · Alexa (documentación e investigación)

---

## 1. Resumen Ejecutivo

BioTracker es una aplicación web interactiva que modela la farmacocinética de suplementos deportivos (cafeína y creatina) usando ecuaciones diferenciales ordinarias. Resuelve cada modelo de **dos formas** — analítica (Transformada de Laplace) y numérica (Método de Euler) — y compara ambas para demostrar el concepto de **error numérico**.

**Estado actual:** La aplicación es **funcional y estable**. El MVP está completo y se encuentra en fase de pulido y expansión de contenido.

---

## 2. Desarrollo Completado ✅

### 2.1 Arquitectura y Core

| Componente | Archivo | Líneas | Estado |
|:---|:---|:---:|:---:|
| Punto de entrada + CSS | `app.py` | 369 | ✅ |
| Launcher Python 3.14+ | `run.py` | 16 | ✅ |
| Dependencias | `requirements.txt` | 5 | ✅ |
| Configuración Git | `.gitignore` | — | ✅ |
| Licencia MIT | `LICENSE` | — | ✅ |

### 2.2 Modelos Matemáticos (`models/`)

| Modelo | Archivo | Líneas | Descripción |
|:---|:---|:---:|:---|
| Cafeína | `caffeine.py` | 241 | Ecuación de Bateman, Laplace simbólico (SymPy), detección de pico/bajón |
| Creatina | `creatine.py` | 241 | Modelo de saturación con fases carga/mantenimiento, estado estable |
| Solver numérico | `solvers.py` | 91 | Método de Euler genérico + cálculo de errores (absoluto, relativo, porcentual) |
| Catálogo cafeína | `caffeine_data.py` | 346 | 22 productos en 3 categorías con marcas, dosis, costos y ka_factor |

### 2.3 Vistas (`views/`)

| Vista | Archivo | Líneas | Descripción |
|:---|:---|:---:|:---|
| Landing page | `home.py` | 291 | Página promocional: problema, solución, audiencia, UTT Tlaxcala |
| Módulo Cafeína | `caffeine_view.py` | 411 | Simulador con entrada dual (manual/catálogo), tarjeta de producto, Modo Pro |
| Módulo Creatina | `creatine_view.py` | 337 | Simulador con fases, gráfica de saturación, Modo Pro |

### 2.4 Features Implementadas

- [x] **Navegación por botones** con estado activo (no dropdown)
- [x] **Landing page promocional** orientada a deportistas, nutricionistas y estudiantes
- [x] **Branding UTT Tlaxcala** — Universidad, carrera, semestre, materia
- [x] **Modelo de cafeína** — Ecuación de Bateman con Laplace paso a paso
- [x] **Modelo de creatina** — Saturación muscular con fases carga/mantenimiento
- [x] **Modo Pro** — Panel colapsable con desarrollo matemático completo
- [x] **Gráficas interactivas** con Plotly (zoom, hover, anotaciones)
- [x] **Tabla de errores numéricos** — Euler vs Analítica con Ea, Er, Er%
- [x] **Catálogo de 22 productos de cafeína** — Natural, Sintética, Liberación Lenta
- [x] **Tarjeta informativa** por producto (marcas, indicaciones, deportes, costos)
- [x] **Factor de absorción (ka_factor)** ajustado automáticamente por producto
- [x] **CSS responsive** — Media queries para tablet (≤1024px), móvil (≤768px), móvil pequeño (≤480px)
- [x] **Compatibilidad light/dark mode** con `@media (prefers-color-scheme)`
- [x] **README.md** profesional con instrucciones, estructura y referencias
- [x] **Repositorio Git** inicializado con historial limpio

### 2.5 Estadísticas del Código

| Métrica | Valor |
|:---|:---:|
| **Total de líneas de código** | ~2,347 |
| **Archivos Python** | 10 |
| **Commits realizados** | 6 |
| **Productos en catálogo** | 22 |
| **Modelos matemáticos** | 2 (cafeína + creatina) |
| **Métodos de resolución** | 2 (Laplace + Euler) |

---

## 3. Pendiente por Implementar 🔲

### 3.1 Desarrollo (Brian)

- [ ] **Tests de usuario** — Verificar en laptops de otros compañeros y resoluciones diferentes
- [ ] **Verificación en Streamlit Cloud** — Hacer deploy en `share.streamlit.io` para link público
- [ ] **Optimización de rendimiento** — Cachear cálculos de Laplace con `@st.cache_data`
- [ ] **Mejoras UX menores** — Feedback visual si surgen bugs del QA de Alexa

### 3.2 Documentación (Alexa)

- [ ] **Reporte académico** — Documento formal con:
  - Portada institucional (UTT, IDGS, 8° semestre)
  - Introducción y planteamiento del problema
  - Marco teórico (farmacocinética, Laplace, Euler, error numérico)
  - Metodología de desarrollo
  - Resultados y capturas de pantalla
  - Conclusiones
  - Referencias bibliográficas (formato IEEE)
- [ ] **Validar constantes farmacocinéticas** — Cruzar valores de ka, ke con fuentes académicas
- [ ] **Probar la app en su laptop** — Verificar que `python run.py` funciona correctamente

### 3.3 QA e Integración (Ambos)

- [ ] **Code review** — Revisión cruzada del código
- [ ] **Fix bugs** reportados durante pruebas
- [ ] **Ensayo de presentación** — Practicar el demo en vivo antes de la entrega

---

## 4. Documentación del Proyecto

### 4.1 Documentación Técnica (en código)

Cada archivo `.py` contiene docstrings detallados que documentan:

- **Propósito del módulo** — Qué problema resuelve
- **Fundamento matemático** — EDOs, constantes, referencias bibliográficas
- **Parámetros** — Valores por defecto y su justificación científica

Ejemplo de estructura de documentación en `models/caffeine.py`:

```text
Ecuación de Bateman:
  C(t) = (k_a · D₀) / ((k_a - k_e) · V_d) · (e^(-k_e·t) - e^(-k_a·t))

Constantes por defecto:
  k_a = 4.0 h⁻¹ (Blanchard & Sawers, 1983)
  k_e = 0.139 h⁻¹ (vida media ~5h, Fredholm et al., 1999)
```

### 4.2 Documentación de Usuario (en la app)

| Sección | Ubicación | Descripción |
|:---|:---|:---|
| Mecanismo de acción | Módulo Cafeína | Qué es la cafeína, antagonista de adenosina |
| ¿Cómo funciona? | Home | 3 etapas: absorción, distribución, eliminación |
| Analogías | Home | Tabla comparativa: Laplace = receta exacta, Euler = ajustar sobre la marcha |
| Modo Pro | Cada módulo | Desarrollo completo de Laplace en 4 pasos |
| Tarjeta de producto | Módulo Cafeína | Indicaciones, contraindicaciones, deportes, marcas, costos |

### 4.3 Documentación Administrativa

| Documento | Estado |
|:---|:---:|
| `README.md` | ✅ Completo |
| `LICENSE` (MIT) | ✅ Completo |
| `DEVELOPMENT_STATUS.md` (este archivo) | ✅ Completo |
| `implementation_plan.md` | ✅ Completo |
| Reporte académico (Word/PDF) | 🔲 Pendiente (Alexa) |

---

## 5. Referencias Bibliográficas

1. Blanchard, J., & Sawers, S. J. A. (1983). *The absolute bioavailability of caffeine in man*. European Journal of Clinical Pharmacology, 24(1), 93-98.
2. Fredholm, B. B., et al. (1999). *Actions of caffeine in the brain with special reference to factors that contribute to its widespread use*. Pharmacological Reviews, 51(1), 83-133.
3. Hultman, E., et al. (1996). *Muscle creatine loading in men*. Journal of Applied Physiology, 81(1), 232-237.
4. Kreider, R. B., et al. (2017). *International Society of Sports Nutrition position stand: safety and efficacy of creatine supplementation*. Journal of the International Society of Sports Nutrition, 14(1), 18.

---

## 6. Stack Tecnológico

| Tecnología | Versión | Propósito |
|:---|:---|:---|
| Python | 3.11+ | Lenguaje base |
| Streamlit | latest | Framework web interactivo |
| SymPy | latest | Resolución simbólica (Transformada de Laplace) |
| NumPy | latest | Cálculos numéricos (Método de Euler) |
| Plotly | latest | Gráficas interactivas |
| Pandas | latest | Tablas de datos y errores |
| Git | latest | Control de versiones |

---

## 7. Historial de Commits

```text
2509e7c  feat: BioTracker v1.0 — MVP completo
9030a8e  Initial commit (LICENSE)
29ea8c6  docs: update README with MIT License and correct repo URL
058219d  Merge branch 'main' (unir LICENSE remoto)
4587ff7  fix: README markdown formatting
6ab698f  feat: catálogo de 22 productos de cafeína + CSS responsive
```

---

> *Este documento se actualiza conforme avanza el desarrollo.*  
> *Última modificación: 24/04/2026 — Brian*
