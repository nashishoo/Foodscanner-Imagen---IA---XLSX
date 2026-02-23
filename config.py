"""
Food Scanner - Configuration Module
Centralized configuration for the application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
IMAGES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-pro"  # Mejor razonamiento para evitar alucinaciones
GEMINI_MAX_TOKENS = 4096
GEMINI_TEMPERATURE = 0.0  # Temperatura 0 para asegurar determinismo y 0 alucinaciones

# Open Food Facts API
OPEN_FOOD_FACTS_BASE_URL = "https://world.openfoodfacts.org"
OPEN_FOOD_FACTS_SEARCH_ENDPOINT = "/cgi/search.pl"
OPEN_FOOD_FACTS_PRODUCT_ENDPOINT = "/api/v0/product"
OPEN_FOOD_FACTS_USER_AGENT = "FoodScanner/1.0"

# OCR Configuration - Multiple products detection
OCR_PROMPT = """Analiza esta imagen (o múltiples imágenes) de una góndola de supermercado o productos alimenticios.
Tu tarea es extraer TODOS los productos distintos que aparecen en las imágenes proporcionadas y devolver el resultado EXCLUSIVAMENTE en formato JSON.

REGLAS CRÍTICAS Y ESTRICTAS (PENALIZACIÓN POR INCUMPLIMIENTO):
1. NO INVENTES NADA: Todo dato que extraigas debe ser 100% fidedigno y explícitamente legible en la imagen. Si no estás seguro de un campo, omítelo.
2. NO DUPLICADOS: Si ves el mismo producto varias veces en las estanterías, DESCARTA los duplicados. Registra el producto una sola vez en el JSON.
3. NO SUMAR CANTIDADES: Asume `cantidad: 1` para todos los productos únicos detectados. No intentes contar cuántas botellas iguales hay, solo registra que ese producto existe en la góndola.
4. EXTRACCIÓN DE METADATOS: Para cada producto distinto, extrae los siguientes campos SI Y SOLO SI son visibles fielmente:
   - "nombre": El nombre del producto exacto. (Obligatorio)
   - "detalle": Peso, volumen o medida legible (ej: "500g", "1L"). (Opcional, si no es visible envía "")
   - "proveedor": Marca principal o fabricante (ej: "Nestle", "Coca-Cola"). (Opcional, si no es visible envía "")
   - "categoria": Deduce la categoría básica ("bebestible", "comida", "helado", "fiambre", "lacteo"). (Opcional, si no es posible envía "")

DEBES devolver el resultado como un ARREGLO JSON válido. No uses markdown ````json ````, devuelve únicamente el texto del JSON puro.
Ejemplo de salida esperada:
[
  {
    "nombre": "Leche Blanca Descremada",
    "detalle": "1L",
    "proveedor": "Soprole",
    "categoria": "lacteo"
  },
  {
    "nombre": "Galletas Tritón",
    "detalle": "",
    "proveedor": "McKay",
    "categoria": "comida"
  }
]

Si no se puede identificar absolutamente ningún producto de manera confiable, devuelve un arreglo JSON vacío: []
"""

# Excel Export Configuration
EXCEL_FILENAME = "food_scan_results.xlsx"
EXCEL_SHEET_NAME = "Productos"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# CLI Defaults
DEFAULT_OUTPUT_FILE = OUTPUT_DIR / EXCEL_FILENAME

# Supported image extensions
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
