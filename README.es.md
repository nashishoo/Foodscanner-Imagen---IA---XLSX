# 🛒 FoodScanner ERP

> **Herramienta para escanear productos de supermercado y generar grillas de inventario para sistemas ERP**
> 
> Construido con 💚 por [Catapaz](https://github.com/catapaz)

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Open Food Facts](https://img.shields.io/badge/Open_Food_Facts-428F7E?style=for-the-badge&logo=open-food-facts&logoColor=white)](https://world.openfoodfacts.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 📌 ¿Qué es FoodScanner ERP?

**FoodScanner ERP** es una herramienta de código abierto que te permite escanear productos de supermercado desde imágenes y generar automáticamente una grilla de inventario lista para importar a tu sistema ERP.

En lugar de escribir manualmente la información de productos o escanear facturas XML, simplemente:
1. Toma una foto de una góndola (estante de tienda) o productos
2. Súbela a la app
3. Obtén una grilla completa con detalles del producto
4. Exporta a CSV/Excel e importa a tu ERP

### 🎯 Casos de Uso

- **Inventario de tienda**: Cataloga rápidamente productos desde fotos de estantes
- **Comparación de precios**: Genera listas de productos para comparación de precios
- **Distribuidores mayoristas**: Crea catálogos de productos desde imágenes de distribuidores
- **Investigación de mercado**: Analiza categorías y marcas en estantes

---

## ✨ Características

- **📸 OCR de Imágenes**: Extrae nombres de productos de imágenes usando Gemini Flash 2.0
- **🔍 Open Food Facts**: Enriquece datos de productos con información nutricional
- **📋 Grilla ERP**: Genera grillas editables con:
  - **Nombre del Producto**
  - **Categoría** (bebestible, comida, helado, fiambre, lacteo)
  - **Proveedor/Marca** (Nestle, Walmart, Soprole, etc.)
  - **Detalle** (peso/volumen: 500g, 1L)
  - **Código de Barra** (o vacío si no está disponible)
- **📥 Exportar**: Descarga como CSV (para ERP) o Excel (datos completos)
- **🌐 Interfaz Web**: UI de Streamlit fácil de usar
- **☁️ Deploy Listo**: Fácil despliegue en Streamlit Cloud

---

## 🚀 Inicio Rápido

### Instalación Local

```bash
# Clona el repositorio
git clone https://github.com/TU_USUARIO/foodscanner-erp.git
cd foodscanner-erp

# Crea un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta la app
streamlit run app.py
```

### Configuración

Crea un archivo `.env` con tu API key de Gemini:

```bash
GEMINI_API_KEY=tu_api_key_aqui
```

Obtén tu API key gratuita en: [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 🎮 Cómo Usar

### 1. Abre la App
Ejecuta `streamlit run app.py` y abre la URL local (generalmente `http://localhost:8501`)

### 2. Sube Imágenes
- Arrastra y suelta imágenes de productos/góndolas
- Soporta: JPG, JPEG, PNG, WebP, BMP

### 3. Procesa
- Haz clic en "Procesar Imágenes"
- La app:
  - Extraerá nombres de productos vía OCR
  - Buscará cada producto en Open Food Facts
  - Mapeará categorías y extraerá detalles

### 4. Revisa y Edita
- Ver la grilla ERP editable
- Corrige manualmente entradas incorrectas
- Selecciona categorías desde dropdown

### 5. Exporta
- **CSV**: Para importación directa a ERP
- **Excel**: Datos completos con información nutricional

---

## ☁️ Desplegar en Streamlit Cloud

Despliega tu propia instancia gratis:

### Paso 1: Sube a GitHub
Sube tu código a un repositorio de GitHub.

### Paso 2: Conecta a Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con GitHub
3. Selecciona tu repositorio
4. Establece el archivo principal como `app.py`

### Paso 3: Agregar Secrets
En la configuración de Streamlit Cloud, agrega tu API key:

```
GEMINI_API_KEY = "tu_api_key_aqui"
```

### Paso 4: Desplegar
Tu app estará disponible en `https://tu-nombre-app.streamlit.app`

---

## 📂 Estructura del Proyecto

```
foodscanner-erp/
├── app.py                 # Interfaz web Streamlit
├── main.py               # Versión CLI (original)
├── config.py            # Configuración
├── requirements.txt     # Dependencias
├── modules/
│   ├── ocr.py          # Procesamiento OCR con Gemini
│   ├── api_client.py   # Cliente de Open Food Facts
│   └── data_handler.py # Manejo de datos y Excel
├── utils/
│   ├── logger.py
│   └── progress.py
└── images/              # Imágenes de entrada (local)
```

---

## 🛠️ Tecnologías

- **Python 3.10+**
- **Streamlit** - Framework de UI web
- **Google Gemini Flash 2.0** - OCR para extracción de texto
- **Open Food Facts API** - Base de datos de productos
- **Pandas** - Manejo de datos
- **OpenPyXL** - Exportación a Excel

---

## 📝 Licencia

Este proyecto está licenciado bajo **MIT License** - eres libre de usar, modificar y distribuir.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Ya sea que quieras:

- 🐛 Reportar errores
- 💡 Sugerir funciones
- 🔧 Enviar pull requests
- 📖 Mejorar documentación

**¡Únete a nosotros para hacer la gestión de inventario más fácil para todos!**

---

## ⚠️ Notas

- **API Keys**: Gemini API tiene un plan gratuito. Consulta [Google AI Studio](https://aistudio.google.com/app/apikey) para los límites.
- **Privacidad**: Las imágenes se procesan en memoria y no se almacenan en servidores.
- **Precisión de Datos**: Siempre verifica la grilla generada antes de importar a tu ERP. Open Food Facts depende de datos contribuidos por la comunidad.

---

## 🏷️ Etiquetas

`#CodigoAbierto` `#ERP` `#Inventario` `#Streamlit` `#Python` `#Supermercado` `#OCR` `#DatosAlimentarios`

---

## 📚 Documentación

- [English](README.md)
- [Español](README.es.md)

---

> **Hecho con 💚 por [Dolan](https://github.com/nashishoo) | [Catapaz](https://www.catapaz.site)**
> 
> *Simplificando la gestión de inventario, una foto a la vez.*
