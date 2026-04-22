# 🧬 BioTracker — Modelado Farmacocinético Interactivo

> **Proyecto Final** · Matemáticas para la Ingeniería II  
> Universidad Tecnológica de Tlaxcala (UTT) · 8° Semestre IDGS · Abril 2026

---

## 📋 Descripción

**BioTracker** es una aplicación web interactiva que modela cómo el cuerpo humano absorbe, distribuye y elimina sustancias bioactivas. Está diseñada para ser útil tanto para **deportistas** y **nutricionistas** como para **estudiantes de ingeniería**.

La aplicación resuelve ecuaciones diferenciales ordinarias (EDOs) de dos formas:

- **Solución Analítica** — Usando la Transformada de Laplace (SymPy)
- **Solución Numérica** — Usando el Método de Euler

Y compara ambas visualmente para demostrar el concepto de **error numérico**.

---

## 🧪 Módulos

### ☕ Cafeína — Modelo Agudo
Simula la concentración plasmática de cafeína tras una dosis oral usando la **Ecuación de Bateman** (modelo de un compartimento con absorción gastrointestinal).

- **EDO:** `dC/dt = (k_a · D₀ · e^(-k_a·t)) / V_d - k_e · C(t)`
- **Escala temporal:** Horas
- **Features:** Detección del pico de energía y del bajón

### 💪 Creatina — Modelo Crónico
Simula la acumulación de fosfocreatina muscular a lo largo de días de suplementación.

- **EDO:** `dS/dt = I - k · S(t)`
- **Escala temporal:** Días/Semanas
- **Features:** Fase de carga vs mantenimiento, porcentaje de saturación

---

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.11 o superior

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/dev-brian/biotracker.git
cd biotracker
```

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python run.py
```

La app se abrirá en tu navegador en `http://localhost:8501`.

---

## 📁 Estructura del Proyecto

```
BioTracker/
├── app.py                  # Punto de entrada principal
├── run.py                  # Launcher con fix Python 3.14
├── requirements.txt        # Dependencias
├── README.md
├── .gitignore
│
├── models/                 # Lógica matemática
│   ├── __init__.py
│   ├── solvers.py          # Método de Euler genérico + errores
│   ├── caffeine.py         # Modelo farmacocinético de cafeína
│   └── creatine.py         # Modelo de saturación de creatina
│
├── views/                  # Interfaz de usuario (Streamlit)
│   ├── __init__.py
│   ├── home.py             # Página de inicio
│   ├── caffeine_view.py    # UI del módulo de cafeína
│   └── creatine_view.py    # UI del módulo de creatina
│
└── assets/                 # Recursos (logos, imágenes)
```

---

## 🛠️ Tecnologías

| Tecnología | Propósito |
|:---|:---|
| **Python 3.11+** | Lenguaje base |
| **Streamlit** | Framework web interactivo |
| **SymPy** | Resolución simbólica (Transformada de Laplace) |
| **NumPy** | Cálculos numéricos (Método de Euler) |
| **Plotly** | Gráficas interactivas |
| **Pandas** | Tablas de datos y errores |

---

## 📐 Fundamento Matemático

### Cafeína — Ecuación de Bateman

La concentración plasmática se obtiene resolviendo el sistema:

```
dD/dt = -k_a · D(t)
dC/dt = (k_a · D(t)) / V_d - k_e · C(t)
```

Aplicando la **Transformada de Laplace** y resolviendo en el dominio de `s`:

```
C(t) = (k_a · D₀) / ((k_a - k_e) · V_d) · (e^(-k_e·t) - e^(-k_a·t))
```

### Creatina — Modelo de Saturación

```
dS/dt = I - k · S(t)
```

Solución por Laplace:

```
S(t) = I/k + (S₀ - I/k) · e^(-k·t)
```

---

## 👥 Equipo

| Nombre | Rol |
|:---|:---|
| **Brian** | Desarrollo de software, arquitectura, implementación |
| **Alexa** | Documentación, testing, investigación científica |

---

## 📚 Referencias

1. Blanchard, J., & Sawers, S. J. A. (1983). *The absolute bioavailability of caffeine in man*. European Journal of Clinical Pharmacology, 24(1), 93-98.
2. Fredholm, B. B., et al. (1999). *Actions of caffeine in the brain with special reference to factors that contribute to its widespread use*. Pharmacological Reviews, 51(1), 83-133.
3. Hultman, E., et al. (1996). *Muscle creatine loading in men*. Journal of Applied Physiology, 81(1), 232-237.
4. Kreider, R. B., et al. (2017). *International Society of Sports Nutrition position stand: safety and efficacy of creatine supplementation*. Journal of the International Society of Sports Nutrition, 14(1), 18.

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.
Proyecto académico — Universidad Tecnológica de Tlaxcala, 2026.
