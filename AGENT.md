# 🤖 Agent Guide - FoodScanner ERP

> Guía para agentes IA que necesiten trabajar con este proyecto

---

## 📁 Estructura del Proyecto

```
foodscanner-erp/
├── app.py                 # Interfaz Streamlit (web)
├── main.py               # Versión CLI original
├── config.py            # Configuración centralizada
├── requirements.txt     # Dependencias Python
├── README.md           # Documentación en inglés
├── README.es.md        # Documentación en español
├── AGENT.md            # Esta guía
├── .env.example        # Ejemplo de variables de entorno
├── .gitignore         # Archivos ignorados
├── modules/
│   ├── __init__.py
│   ├── ocr.py         # OCR con Gemini API
│   ├── api_client.py  # Cliente Open Food Facts
│   └── data_handler.py # Procesamiento de datos y Excel
└── utils/
    ├── __init__.py
    ├── logger.py       # Logging
    └── progress.py    # Progress bars
```

---

## 🎯 Propósito del Proyecto

FoodScanner ERP es una herramienta diseñada originalmente como un **complemento para [Micro-ERP-Minimarket](https://github.com/nashishoo/Micro-ERP-Minimarket)** que:
1. **Recibe imágenes** de productos/góndolas de supermercado
2. **Extrae nombres** de productos usando OCR (Gemini API)
3. **Busca en Open Food Facts** para obtener datos nutricionales
4. **Genera una grilla editable** con: Nombre, Categoría, Proveedor, Detalle, Código de Barra
5. **Exporta a CSV/Excel** para importar a sistemas ERP (como Micro-ERP-Minimarket)

---

## ⚙️ Configuración Requerida

### Variables de Entorno

El proyecto usa un archivo `.env` (NO subir a GitHub - ya está en .gitignore):

```bash
GEMINI_API_KEY=tu_api_key_de_gemini
```

Obtener API key: https://aistudio.google.com/app/apikey

### Dependencias

```bash
pip install -r requirements.txt
```

Paquetes principales:
- `streamlit` - Interfaz web
- `google-generativeai` - OCR con Gemini
- `pandas` - Manejo de datos
- `openpyxl` - Exportación Excel
- `requests` - HTTP para API
- `python-dotenv` - Cargar .env

---

## 🚀 Cómo Ejecutar

### Desarrollo Local

```bash
# En la carpeta del proyecto
cd "C:\Users\Ignacio\Desktop\Foodscan fast"

# Ejecutar interfaz web (recomendado)
streamlit run app.py

# O ejecutar versión CLI
python main.py --input images/
```

### Producción (Streamlit Cloud)

1. Subir código a GitHub
2. Conectar repo a https://share.streamlit.io
3. En Settings > Secrets agregar:
   ```
   GEMINI_API_KEY = "tu_api_key"
   ```
4. Deploy automático

---

## 📝 Descripción de Módulos

### `app.py` (Interfaz Streamlit)

**Propósito**: Interfaz visual web

**Funciones principales**:
- `init_session_state()` - Inicializa variables de sesión
- `process_images()` - Procesa imágenes cargadas
- `display_erp_grid()` - Muestra grilla editable
- `add_footer()` - Footer con créditos (Dolan | Catapaz)
- `main()` - Función principal

**Notas importantes**:
- Usa `load_dotenv()` para cargar API key
- Procesa imágenes en directorio temporal
- Exporta a CSV y Excel en memoria (BytesIO)

---

### `modules/ocr.py` (OCR)

**Propósito**: Extraer nombres de productos de imágenes

**Clase principal**: `OCRProcessor`

**Métodos**:
- `__init__(api_key, demo_mode)` - Inicializa con API key o modo demo
- `process_image(image_path)` - Procesa una imagen, retorna lista de productos
- `process_batch(image_paths)` - Procesa múltiples imágenes

**Demo mode**: Retorna productos mock sin necesidad de API key

---

### `modules/api_client.py` (Open Food Facts)

**Propósito**: Consultar base de datos de productos

**Clase principal**: `OpenFoodFactsClient`

**Métodos**:
- `search_product(product_name)` - Busca producto por nombre
- `get_product_by_barcode(barcode)` - Busca por código de barras
- `_parse_product_data(product)` - Normaliza datos del API

**Datos que extrae**:
- code, product_name, brands, categories
- quantity, serving_size (para campo "detalle")
- nutriments (energía, macros, etc.)

---

### `modules/data_handler.py` (Datos)

**Propósito**: Procesar y formatear datos para ERP

**Clase principal**: `DataHandler`

**Métodos**:
- `add_result()` - Agrega resultado con mapeo de campos ERP
- `export_to_excel()` - Exporta a Excel
- `get_summary()` - Retorna estadísticas
- `_extract_category_from_openfood()` - Mapea categorías
- `_extract_quantity_from_openfood()` - Extrae gramaje/volumen
- `_extract_brand_as_proveedor()` - Normaliza marca como proveedor

**Campos ERP generados**:
- `nombre` - Nombre del producto
- `categoria` - bebestible, comida, helado, fiambre, lacteo
- `proveedor` - Marca (Nestle, Walmart, etc.)
- `detalle` - Gramaje (500g, 1L)
- `codigo_barra` - Código de barras

---

## 🔧 Buenas Prácticas para Modificar

### NO ROMPER:

1. **No cambiar nombres de funciones exportadas** en `modules/__init__.py`
2. **Mantener estructura de datos** - El frontend espera ciertos campos
3. **No hardcodear API keys** - Usar siempre `.env` o secrets
4. **No guardar imágenes** en servidor - Usar temp directories

### SI HACER:

1. **Probar cambios localmente** antes de push
2. **Usar modo demo** (`demo_mode=True`) para testing sin API key
3. **Agregar logs** usando el logger existente
4. **Testear exports** (CSV y Excel) después de cambios

---

## 🐛 Troubleshooting Común

### Error: "API key no proporcionada"
- Verificar que `.env` existe y tiene `GEMINI_API_KEY`
- En Streamlit Cloud: verificar secrets

### Error: "Permission denied" en Excel
- Ya corregido: usar `BytesIO` en lugar de archivo temporal
- Si vuelve a ocurrir, revisar cómo se exporta en `app.py`

### Error: "No se encuentran productos"
- Open Food Facts depende de la base de datos pública
- Algunos productos locales pueden no estar
- Verificar conexión a internet

### Warning: google.generativeai deprecated
- Funciona igual por ahora
- Para actualizar: cambiar a paquete `google.genai`

---

## 📤 Deploy Checklist

Antes de hacer deploy:

- [ ] Probar localmente con `streamlit run app.py`
- [ ] Verificar que `.env` NO está en el repo
- [ ] Verificar `requirements.txt` tiene todas las dependencias
- [ ] Probar modo demo funciona
- [ ] Verificar footer con créditos

En Streamlit Cloud:

- [ ] Conectar repositorio
- [ ] Agregar GEMINI_API_KEY en Secrets
- [ ] Verificar archivo principal (app.py o streamlit_app.py)

---

## 📞 Contacto

- **Dolan**: https://github.com/nashishoo

---

*Última actualización: Febrero 2026*
