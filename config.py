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
GEMINI_MODEL = "gemini-2.0-flash"  # Gemini Flash 2.0
GEMINI_MAX_TOKENS = 2048
GEMINI_TEMPERATURE = 0.1

# Open Food Facts API
OPEN_FOOD_FACTS_BASE_URL = "https://world.openfoodfacts.org"
OPEN_FOOD_FACTS_SEARCH_ENDPOINT = "/cgi/search.pl"
OPEN_FOOD_FACTS_PRODUCT_ENDPOINT = "/api/v0/product"
OPEN_FOOD_FACTS_USER_AGENT = "FoodScanner/1.0"

# OCR Configuration - Multiple products detection
OCR_PROMPT = """Analiza esta imagen de una gondola de supermercado o productos alimenticios.
Extrae TODOS los nombres de productos que aparezcan en la imagen.
Devuelve una LISTA SEPARADA POR COMAS de todos los productos que identifiques.
No incluya descripciones, solo los nombres de los productos.
Ejemplo de respuesta: Producto A, Producto B, Producto C
Si no puedes identificar productos, responde: "NO_DETECTADO"
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
