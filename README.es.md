<div align="center">

# 🛒 FoodScanner ERP

**Transforma fotos de estantes en datos de inventario en segundos.**<br>
Una herramienta complementaria inteligente para [Micro-ERP-Minimarket](https://github.com/nashishoo/Micro-ERP-Minimarket) que extrae automáticamente información de productos desde góndolas de supermercado usando IA.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Open Food Facts](https://img.shields.io/badge/Open_Food_Facts-428F7E?style=for-the-badge&logo=open-food-facts&logoColor=white)](https://world.openfoodfacts.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

[English](README.md) • [Guía del Agente](AGENT.md) • [Reportar Error](https://github.com/nashishoo/foodscanner-erp/issues)

</div>

---

## 📌 Visión General

**FoodScanner ERP** elimina el tedioso proceso de ingresar el inventario manualmente. Simplemente tomando una foto de un estante de la tienda, esta herramienta usa OCR de vanguardia (Gemini Flash 2.0) y la base de datos de Open Food Facts para generar instantáneamente una grilla de inventario completa y editable, lista para tu sistema ERP.

Diseñado específicamente como un complemento para el ecosistema [Micro-ERP-Minimarket](https://github.com/nashishoo/Micro-ERP-Minimarket), pero lo suficientemente flexible para funcionar con cualquier sistema que acepte importaciones de archivos CSV.

### 📸 Demostración

| Interfaz de la Web App | Proceso de Escaneo | Grilla Generada |
| :---: | :---: | :---: |
| <img src="https://postimg.cc/87DYv7pY" alt="Interfaz de la Web App" width="250"/> | <img src="https://postimg.cc/w1VGQ9MP" alt="Proceso de Escaneo" width="250"/> | <img src="https://postimg.cc/NK4zkQLB" alt="Grilla Generada" width="250"/> |

---

## ✨ Características

- **📸 OCR potenciado por IA**: Extrae nombres de productos instantáneamente a partir de imágenes usando Gemini Flash 2.0.
- **🔍 Auto-Enriquecimiento**: Obtiene información nutricional, categorías y códigos de barras a través de Open Food Facts.
- **📋 Categorización Inteligente**: Agrupa artículos automáticamente en categorías como *bebestible, comida, helado, fiambre, lacteo*.
- **⚡ Listo para ERP**: Genera grillas editables mapeando detalles como peso/volumen (ej., 500g, 1L) y Marca/Proveedor.
- **📥 Exportación en un clic**: Descarga como CSV para importación directa al ERP, o en Excel para bases de datos completas.
- **🌐 Interfaz Web**: Interfaz limpia y amigable para el usuario construida en Streamlit.
- **☁️ Listo para la Nube**: Despliegue con un botón a Streamlit Cloud.

---

## 🚀 Inicio Rápido

Pon a correr FoodScanner ERP localmente en menos de 2 minutos.

### Requisitos Previos
- Python 3.10+
- Una [Google Gemini API Key](https://aistudio.google.com/app/apikey) gratuita.

### Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/nashishoo/foodscanner-erp.git
cd foodscanner-erp

# 2. Crea y activa el entorno virtual
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Configura tu API key
echo "GEMINI_API_KEY=tu_api_key_aqui" > .env

# 5. Ejecuta la aplicación
streamlit run app.py
```

La app se abrirá instantáneamente en tu navegador en `http://localhost:8501`.

---

## 🎮 Guía de Uso

1. **Sube Imágenes**: Arrastra y suelta fotos de productos o góndolas (soporta JPG, WebP, PNG).
2. **Procesa**: Haz clic en "Procesar Imágenes". La IA se encarga de la extracción de texto y la búsqueda de datos automáticamente.
3. **Revisa y Edita**: Revisa la grilla generada en la interfaz web. Puedes ajustar manualmente cualquier campo, seleccionar categorías del menú desplegable o corregir errores tipográficos.
4. **Exporta**: 
   - Elige **CSV** para importar directamente los datos limpios en [Micro-ERP-Minimarket](https://github.com/nashishoo/Micro-ERP-Minimarket) o en tu sistema de preferencia.
   - Elige **Excel** para mantener un registro local y legible por humanos con datos expandidos.

---

## ☁️ Despliegue

Despliega tu propia instancia en Streamlit Cloud de forma gratuita:

1. Empuja (push) tu repositorio local a GitHub.
2. Visita [share.streamlit.io](https://share.streamlit.io) e inicia sesión.
3. Selecciona tu repositorio y establece la ruta del archivo principal como `app.py`.
4. En "Advanced Settings" (Configuraciones Avanzadas), añade tu Clave API de Gemini directamente en la sección **Secrets**:
   ```toml
   GEMINI_API_KEY = "tu_api_key_aqui"
   ```
5. Haz clic en **Deploy!**

---

## 📂 Estructura del Proyecto

```text
foodscanner-erp/
├── app.py                 # Punto de entrada de interfaz web Streamlit
├── main.py                # Versión CLI antigua
├── config.py              # Configuración centralizada
├── modules/
│   ├── ocr.py             # Lógica de procesamiento OCR con Gemini
│   ├── api_client.py      # Integración con API Open Food Facts
│   └── data_handler.py    # Manejo de exportación y estructura de datos
└── utils/                 # Utilidades compartidas (logs, barras de progreso)
```

---

## 🤝 Contribuir

Las contribuciones son las que hacen que la comunidad de código abierto sea un lugar increíble para aprender, inspirarse y crear. Cualquier contribución que hagas será **enormemente apreciada**.

1. Haz un Fork del proyecto
2. Crea tu Rama de Característica (`git checkout -b feature/CaracteristicaIncreible`)
3. Haz un Commit de tus cambios (`git commit -m 'Agregar alguna CaracteristicaIncreible'`)
4. Haz un Push a la Rama (`git push origin feature/CaracteristicaIncreible`)
5. Abre un Pull Request

---

## 📝 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

---

<div align="center">
  <p>Hecho con 💚 por <a href="https://github.com/nashishoo">Dolan</a> | <a href="https://www.catapaz.site">Catapaz</a></p>
  <p><i>Simplificando la gestión de inventario, una foto a la vez.</i></p>
</div>
