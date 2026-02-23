<div align="center">

# 🛒 FoodScanner ERP

**Transform shelf photos into inventory data in seconds.**<br>
A smart companion tool for [Micro-ERP-Minimarket](https://github.com/nashishoo/Micro-ERP-Minimarket) that automatically extracts product information from supermarket shelves using AI.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Open Food Facts](https://img.shields.io/badge/Open_Food_Facts-428F7E?style=for-the-badge&logo=open-food-facts&logoColor=white)](https://world.openfoodfacts.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

[Español](README.es.md) • [Agent Guide](AGENT.md) • [Report Bug](https://github.com/nashishoo/foodscanner-erp/issues)

</div>

---

## 📌 Overview

**FoodScanner ERP** eliminates the tedious process of manual inventory entry. By simply snapping a photo of a store shelf, this tool uses cutting-edge OCR (Gemini Flash 2.0) and the Open Food Facts database to instantly generate a complete, editable inventory grid ready for your ERP system.

Designed specifically as a companion to the [Micro-ERP-Minimarket](https://github.com/nashishoo/Micro-ERP-Minimarket) ecosystem, but flexible enough to work with any system that accepts CSV imports.

### 📸 Showcase

| Web App Interface | Scanning Process | Generated Grid |
| :---: | :---: | :---: |
| <img src="https://i.postimg.cc/R4gCJQdJ/api-scan.png" alt="Web App Interface" width="250"/> | <img src="https://i.postimg.cc/y7W1mgpS/scan-default.jpg" alt="Scanning Process" width="250"/> | <img src="https://i.postimg.cc/SmjS621r/scan-work.jpg" alt="Generated Grid" width="250"/> |

---

## ✨ Features

- **📸 AI-Powered OCR**: Extracts product names instantly from images using Gemini Flash 2.0.
- **🔍 Auto-Enrichment**: Fetches nutritional info, categories, and barcodes via Open Food Facts.
- **📋 Smart Categorization**: Automatically groups items into categories like *bebestible, comida, helado, fiambre, lacteo*.
- **⚡ ERP Ready**: Generates editable grids mapping details like weight/volume (e.g., 500g, 1L) and Brand/Supplier.
- **📥 One-Click Export**: Download as CSV for direct ERP import, or Excel for complete datasets.
- **🌐 Web Interface**: Clean, user-friendly UI built on Streamlit.
- **☁️ Cloud Ready**: Push-button deployment to Streamlit Cloud.

---

## 🚀 Quick Start

Get FoodScanner ERP running locally in under 2 minutes.

### Prerequisites
- Python 3.10+
- A free [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/nashishoo/foodscanner-erp.git
cd foodscanner-erp

# 2. Create and activate virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 5. Launch the app
streamlit run app.py
```

The app will instantly open in your browser at `http://localhost:8501`.

---

## 🎮 Usage Guide

1. **Upload Images**: Drag and drop photos of products or gondolas (JPG, WebP, PNG supported).
2. **Process**: Click "Process Images". The AI handles the text extraction and data matching automatically.
3. **Review & Edit**: Review the generated grid in the UI. You can manually adjust any fields, select categories from dropdowns, or correct typos.
4. **Export**: 
   - Choose **CSV** to immediately import the clean data into [Micro-ERP-Minimarket](https://github.com/nashishoo/Micro-ERP-Minimarket) or your system of choice.
   - Choose **Excel** to keep a local, human-readable record with extended data.

---

## ☁️ Deployment

Deploy your own instance to Streamlit Cloud for free:

1. Push your local repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and log in.
3. Select your repository and set the main file path to `app.py`.
4. In the "Advanced Settings", add your Gemini API Key directly into the **Secrets** section:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
5. Click **Deploy!**

---

## 📂 Project Structure

```text
foodscanner-erp/
├── app.py                 # Streamlit web interface entry point
├── main.py                # Legacy CLI version
├── config.py              # Centralized configuration
├── modules/
│   ├── ocr.py             # Gemini OCR processing logic
│   ├── api_client.py      # Open Food Facts API integration
│   └── data_handler.py    # Data structuring & export handling
└── utils/                 # Shared utilities (logging, progress)
```

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <p>Made with 💚 by <a href="https://github.com/nashishoo">Dolan</a> | <a href="https://www.catapaz.site">Catapaz</a></p>
  <p><i>Simplifying inventory management, one photo at a time.</i></p>
</div>
