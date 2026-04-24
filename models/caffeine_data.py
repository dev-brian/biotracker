"""
BioTracker — Base de Datos de Fuentes de Cafeína
==================================================
Catálogo completo de productos con cafeína, clasificados por tipo de absorción.
Investigación validada por fuentes farmacéuticas y nutricionales.

Categorías:
  - Natural: Fuentes extraídas directamente de alimentos o plantas
  - Sintética: Aislada químicamente para absorción rápida
  - Liberación Lenta: Formulaciones para energía sostenida
"""

CATEGORIAS = {
    "🌿 Natural": {
        "descripcion": "Fuentes extraídas directamente de alimentos o plantas.",
        "color": "#4ecdc4",
    },
    "⚡ Sintética": {
        "descripcion": "Aislada químicamente para absorción rápida y concentraciones precisas.",
        "color": "#f59e0b",
    },
    "🕐 Liberación Lenta": {
        "descripcion": "Formulaciones diseñadas para evitar picos rápidos y mantener energía durante horas.",
        "color": "#a78bfa",
    },
}

# ============================================================================
# CATÁLOGO DE PRODUCTOS
# Cada producto tiene:
#   - nombre: Nombre comercial / común
#   - categoria: Clave de CATEGORIAS
#   - mg_min, mg_max: Rango de cafeína por porción (mg)
#   - dosis_recomendada: Texto con la dosis sugerida
#   - marcas: Lista de marcas representativas
#   - indicado: Para quién es recomendable
#   - contraindicado: Para quién NO es recomendable
#   - costo: Rango de precio estimado (MXN)
#   - deportes: Lista de deportes sugeridos
#   - ka_factor: Factor de modificación de k_a respecto al default (1.0 = normal)
#                Valores > 1 = absorción más rápida, < 1 = más lenta
# ============================================================================

PRODUCTOS = [
    # ======================== NATURALES ========================
    {
        "nombre": "Espresso",
        "categoria": "🌿 Natural",
        "mg_min": 60, "mg_max": 80,
        "dosis_recomendada": "1-2 tazas/día (máx. 200 mg)",
        "marcas": ["Nespresso", "Lavazza", "Illy", "Blue Bottle", "Intelligentsia"],
        "indicado": "Adultos sanos",
        "contraindicado": "Personas con gastritis o ansiedad",
        "costo": "$30-60 MXN",
        "deportes": ["Pesas", "Sprint", "Artes marciales"],
        "ka_factor": 1.0,
    },
    {
        "nombre": "Café filtrado / Americano",
        "categoria": "🌿 Natural",
        "mg_min": 90, "mg_max": 120,
        "dosis_recomendada": "2-3 tazas/día (máx. 300 mg)",
        "marcas": ["Café Garat", "La Finca", "Leyenda Gourmet", "El Marino", "Grano Legal"],
        "indicado": "Cuerpos más densos",
        "contraindicado": "Hipertensos o con insomnio",
        "costo": "$20-60 MXN",
        "deportes": ["Ciclismo", "Maratón", "Triatlón"],
        "ka_factor": 0.9,
    },
    {
        "nombre": "Prensa francesa",
        "categoria": "🌿 Natural",
        "mg_min": 80, "mg_max": 110,
        "dosis_recomendada": "1-2 tazas/día",
        "marcas": ["Café Richard", "Molongo", "Lobodis", "Cafés Verlet", "Café Lomi"],
        "indicado": "Cuerpos más densos",
        "contraindicado": "Personas con colesterol alto",
        "costo": "$300-400 MXN/kg",
        "deportes": ["CrossFit", "Fútbol", "Básquetbol"],
        "ka_factor": 0.85,
    },
    {
        "nombre": "Moka italiana",
        "categoria": "🌿 Natural",
        "mg_min": 90, "mg_max": 120,
        "dosis_recomendada": "1-2 porciones/día",
        "marcas": ["Granell", "Lavazza Qualità Rossa", "Caffè Vergnano", "NOVELL"],
        "indicado": "Adultos sanos",
        "contraindicado": "Personas con nerviosismo o arritmias",
        "costo": "$170-900 MXN/kg",
        "deportes": ["Halterofilia", "Boxeo"],
        "ka_factor": 0.95,
    },
    {
        "nombre": "Cold Brew",
        "categoria": "🌿 Natural",
        "mg_min": 150, "mg_max": 200,
        "dosis_recomendada": "1 taza/día (muy concentrado)",
        "marcas": ["Dan's Café", "Unánumo", "KEX", "Café la Nacional", "Almaquieta"],
        "indicado": "Atletas de resistencia",
        "contraindicado": "Embarazadas, adolescentes, insomnio",
        "costo": "$50-180 MXN / 250 ml",
        "deportes": ["Ultramaratón", "Ciclismo de ruta"],
        "ka_factor": 0.75,
    },
    {
        "nombre": "Café turco / árabe",
        "categoria": "🌿 Natural",
        "mg_min": 70, "mg_max": 100,
        "dosis_recomendada": "1-2 tazas/día",
        "marcas": ["Lavazza", "Illy", "Kurukahveci Mehmet Efendi", "Nespresso", "Selamlique"],
        "indicado": "Adultos sanos",
        "contraindicado": "Personas con problemas digestivos",
        "costo": "$200-400 MXN/kg",
        "deportes": ["Natación", "Remo"],
        "ka_factor": 0.9,
    },
    {
        "nombre": "Café instantáneo",
        "categoria": "🌿 Natural",
        "mg_min": 60, "mg_max": 90,
        "dosis_recomendada": "2-3 tazas/día",
        "marcas": ["Nescafé", "Jacobs Gourmet", "Juan Valdez", "Punta del Cielo", "Dolca"],
        "indicado": "Adultos mayores",
        "contraindicado": "Menores de 18 años, personas con migraña",
        "costo": "$80-200 MXN",
        "deportes": ["Deportes recreativos", "Baja intensidad"],
        "ka_factor": 1.1,
    },
    {
        "nombre": "Descafeinado soluble",
        "categoria": "🌿 Natural",
        "mg_min": 1, "mg_max": 4,
        "dosis_recomendada": "1-2 tazas/día",
        "marcas": ["Nescafé Descafeinado", "Oro Descafeinado", "Jacobs Descafeinado"],
        "indicado": "Trabajadores o estudiantes",
        "contraindicado": "Síndrome de intestino irritable",
        "costo": "$50-180 MXN",
        "deportes": ["eSports", "Estudios prolongados"],
        "ka_factor": 1.0,
    },
    {
        "nombre": "Té verde (240 ml)",
        "categoria": "🌿 Natural",
        "mg_min": 25, "mg_max": 40,
        "dosis_recomendada": "2-3 tazas/día (máx. 300 mg/día)",
        "marcas": ["TRESSO", "Hema", "Tecnobotánica de México", "Therbal", "Tetley"],
        "indicado": "Personas que buscan energía moderada",
        "contraindicado": "Anémicos y en gastritis",
        "costo": "$28-100 MXN / 20-25 sobres",
        "deportes": ["Running", "Ciclismo", "Natación"],
        "ka_factor": 0.7,
    },
    {
        "nombre": "Té negro (240 ml)",
        "categoria": "🌿 Natural",
        "mg_min": 60, "mg_max": 70,
        "dosis_recomendada": "1-2 tazas/día",
        "marcas": ["TRESSO", "KEX / Euro Té", "Tea Forté", "Tetley Premium"],
        "indicado": "Adultos sanos",
        "contraindicado": "Hipertensos y ansiosos",
        "costo": "$175-300 MXN",
        "deportes": ["Artes marciales", "Halterofilia"],
        "ka_factor": 0.75,
    },
    {
        "nombre": "Té matcha (240 ml)",
        "categoria": "🌿 Natural",
        "mg_min": 60, "mg_max": 70,
        "dosis_recomendada": "1-2 tazas/día",
        "marcas": ["Nature's Heart", "Zoma Tea", "Kumoritea", "Bulk"],
        "indicado": "Atletas que necesitan energía sostenida",
        "contraindicado": "Personas con insomnio o ansiedad",
        "costo": "$150-278 MXN / 100g",
        "deportes": ["Yoga", "Escalada", "Triatlón"],
        "ka_factor": 0.6,
    },
    {
        "nombre": "Chocolate oscuro (30g, 70% cacao)",
        "categoria": "🌿 Natural",
        "mg_min": 20, "mg_max": 40,
        "dosis_recomendada": "1-2 porciones/día",
        "marcas": ["Lindt", "Turing", "ChocoZero", "Hershey's"],
        "indicado": "Adultos sanos",
        "contraindicado": "Diabéticos o personas con migrañas sensibles a cacao",
        "costo": "$21-25 MXN / 16g",
        "deportes": ["Sprint", "HIIT", "Deportes de contacto"],
        "ka_factor": 0.5,
    },
    {
        "nombre": "Cacao puro en polvo (10g)",
        "categoria": "🌿 Natural",
        "mg_min": 10, "mg_max": 25,
        "dosis_recomendada": "1-2 porciones/día",
        "marcas": ["AQP 100% Natural", "Sevenhills Wholefoods", "Indigo Herbs", "Okko"],
        "indicado": "Adultos sanos",
        "contraindicado": "Personas con colon irritable o gastritis",
        "costo": "$175-300 MXN",
        "deportes": ["Atletismo", "Calistenia"],
        "ka_factor": 0.45,
    },

    # ======================== SINTÉTICAS ========================
    {
        "nombre": "Tabletas / cápsulas de cafeína anhidra",
        "categoria": "⚡ Sintética",
        "mg_min": 100, "mg_max": 200,
        "dosis_recomendada": "1 cápsula antes del ejercicio (máx. 400 mg/día)",
        "marcas": ["Olympian", "Cafiaspirina", "Vivitar", "Force Factor", "Elite"],
        "indicado": "Atletas de resistencia",
        "contraindicado": "Hipertensos, ansiosos, embarazadas, arritmias",
        "costo": "$175-300 MXN",
        "deportes": ["Maratón", "Ciclismo", "Triatlón"],
        "ka_factor": 1.5,
    },
    {
        "nombre": "Geles / shots deportivos",
        "categoria": "⚡ Sintética",
        "mg_min": 25, "mg_max": 100,
        "dosis_recomendada": "1-2 durante esfuerzos >90 min",
        "marcas": ["GU", "SiS Go", "NT Nutrition", "Dextro Energy", "Hüma"],
        "indicado": "Corredores y ciclistas",
        "contraindicado": "Personas con problemas gastrointestinales",
        "costo": "$60-100 MXN / pieza",
        "deportes": ["Maratón", "Ciclismo de ruta", "Triatlón"],
        "ka_factor": 1.8,
    },
    {
        "nombre": "Polvo de cafeína anhidra (bulk)",
        "categoria": "⚡ Sintética",
        "mg_min": 100, "mg_max": 400,
        "dosis_recomendada": "Máx. 400 mg/día (requiere balanza de precisión)",
        "marcas": ["Bulk Supplements", "Siegfried", "Power Natural Life", "Green Depot"],
        "indicado": "Atletas avanzados con experiencia",
        "contraindicado": "Uso casero sin supervisión",
        "costo": "$175-300 MXN",
        "deportes": ["No recomendado recreativamente"],
        "ka_factor": 2.0,
    },
    {
        "nombre": "Pre-workouts con cafeína anhidra",
        "categoria": "⚡ Sintética",
        "mg_min": 150, "mg_max": 300,
        "dosis_recomendada": "1 porción 30 min antes del entrenamiento",
        "marcas": ["Psychotic", "C4", "Primal", "Hyde Nightmare", "Gorilla Mode", "Pandamic"],
        "indicado": "Personas que buscan potencia y concentración",
        "contraindicado": "Insomnio, ansiedad o reflujo",
        "costo": "$800-4000 MXN",
        "deportes": ["Halterofilia", "CrossFit", "HIIT", "Powerlifting"],
        "ka_factor": 1.6,
    },
    {
        "nombre": "Chicles con cafeína anhidra",
        "categoria": "⚡ Sintética",
        "mg_min": 40, "mg_max": 100,
        "dosis_recomendada": "1-2 piezas según necesidad",
        "marcas": ["Neurogum", "Onegum", "Stay Alert", "Kafewake"],
        "indicado": "Deportistas y militares (efecto inmediato)",
        "contraindicado": "Diabéticos o alérgicos a cacao",
        "costo": "$200-800 MXN",
        "deportes": ["Fútbol", "Artes marciales", "eSports"],
        "ka_factor": 2.2,
    },

    # ======================== LIBERACIÓN LENTA ========================
    {
        "nombre": "Geles deportivos con cafeína sostenida",
        "categoria": "🕐 Liberación Lenta",
        "mg_min": 25, "mg_max": 75,
        "dosis_recomendada": "1-2 durante entrenamientos largos (>2h)",
        "marcas": ["Dextrosa", "GU", "Ruts"],
        "indicado": "Personas que requieren energía gradual",
        "contraindicado": "Personas con problemas gastrointestinales",
        "costo": "$45-100 MXN",
        "deportes": ["Maratón", "Ciclismo", "Ironman"],
        "ka_factor": 0.3,
    },
    {
        "nombre": "Tabletas combinadas (cafeína + teanina)",
        "categoria": "🕐 Liberación Lenta",
        "mg_min": 150, "mg_max": 250,
        "dosis_recomendada": "1 dosis al inicio del entrenamiento",
        "marcas": ["True Athlete", "Tabletas combinadas"],
        "indicado": "Atletas que buscan energía prolongada",
        "contraindicado": "Personas con insomnio, ansiedad o reflujo",
        "costo": "$300-1000 MXN",
        "deportes": ["Triatlón", "Ultramaratones", "Deportes de precisión"],
        "ka_factor": 0.35,
    },
    {
        "nombre": "Polvos pre-entrenamiento time-release",
        "categoria": "🕐 Liberación Lenta",
        "mg_min": 150, "mg_max": 300,
        "dosis_recomendada": "1 porción 30 min antes del entrenamiento",
        "marcas": ["Boogieman", "RSP Nutrition", "Pre-X"],
        "indicado": "Deportistas que requieren energía sostenida",
        "contraindicado": "Personas sensibles a estimulantes múltiples",
        "costo": "$400-1300 MXN",
        "deportes": ["CrossFit", "Halterofilia", "Fútbol", "Básquetbol"],
        "ka_factor": 0.3,
    },
    {
        "nombre": "Cápsulas de liberación prolongada",
        "categoria": "🕐 Liberación Lenta",
        "mg_min": 100, "mg_max": 200,
        "dosis_recomendada": "1 cápsula 1-2 veces al día (máx. 400 mg/día)",
        "marcas": ["BareLabs", "Bioelectro", "HSN CaffXtend", "Durvitan"],
        "indicado": "Personas que necesitan energía estable durante horas",
        "contraindicado": "Hipertensos, embarazadas o problemas cardíacos",
        "costo": "$160-300 MXN",
        "deportes": ["Maratón", "Ciclismo de ruta", "Senderismo"],
        "ka_factor": 0.25,
    },
]


def obtener_por_categoria(categoria):
    """Filtra productos por categoría."""
    return [p for p in PRODUCTOS if p["categoria"] == categoria]


def obtener_nombres_por_categoria(categoria):
    """Devuelve los nombres de productos de una categoría."""
    return [p["nombre"] for p in PRODUCTOS if p["categoria"] == categoria]


def obtener_producto(nombre):
    """Busca un producto por nombre."""
    for p in PRODUCTOS:
        if p["nombre"] == nombre:
            return p
    return None


def dosis_promedio(producto):
    """Calcula la dosis promedio de un producto (punto medio del rango)."""
    return (producto["mg_min"] + producto["mg_max"]) / 2


def obtener_todos_deportes():
    """Devuelve lista única de todos los deportes mencionados."""
    deportes = set()
    for p in PRODUCTOS:
        for d in p["deportes"]:
            deportes.add(d)
    return sorted(deportes)
