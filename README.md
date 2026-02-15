# 🛒 FoodScanner ERP

> **Tool for scanning supermarket products and generating inventory grids for ERP systems**
> 
> Built with 💚 by [Catapaz](https://github.com/catapaz)

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Open Food Facts](https://img.shields.io/badge/Open_Food_Facts-428F7E?style=for-the-badge&logo=open-food-facts&logoColor=white)](https://world.openfoodfacts.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 📌 What is FoodScanner ERP?

**FoodScanner ERP** is an open-source tool that allows you to scan supermarket products from images and automatically generate an inventory grid ready to import into your ERP system.

Instead of manually typing product information or scanning XML invoices, you simply:
1. Take a photo of a gondola (store shelf) or products
2. Upload it to the app
3. Get a complete grid with product details
4. Export to CSV/Excel and import to your ERP

### 🎯 Use Cases

- **Store inventory**: Quickly catalog products from shelf photos
- **Price comparison**: Generate product lists for comparison shopping
- **Wholesale distributors**: Create product catalogs from distributor images
- **Market research**: Analyze product categories and brands on shelves

---

## ✨ Features

- **📸 Image OCR**: Extracts product names from images using Gemini Flash 2.0
- **🔍 Open Food Facts**: Enriches product data with nutritional information
- **📋 ERP Grid**: Generates editable grids with:
  - **Product Name**
  - **Category** (bebestible, comida, helado, fiambre, lacteo)
  - **Supplier/Brand** (Nestle, Walmart, Soprole, etc.)
  - **Details** (weight/volume: 500g, 1L)
  - **Barcode** (or blank if not available)
- **📥 Export**: Download as CSV (for ERP) or Excel (full data)
- **🌐 Web Interface**: User-friendly Streamlit UI
- **☁️ Deploy Ready**: Easy deployment to Streamlit Cloud

---

## 🚀 Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/foodscanner-erp.git
cd foodscanner-erp

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Configuration

Create a `.env` file with your Gemini API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

Get your free API key at: [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 🎮 How to Use

### 1. Open the App
Run `streamlit run app.py` and open the local URL (usually `http://localhost:8501`)

### 2. Upload Images
- Drag and drop images of products/gondolas
- Supports: JPG, JPEG, PNG, WebP, BMP

### 3. Process
- Click "Process Images"
- The app will:
  - Extract product names via OCR
  - Search each product in Open Food Facts
  - Map categories and extract details

### 4. Review & Edit
- View the editable ERP grid
- Manually correct any wrong entries
- Select categories from dropdown

### 5. Export
- **CSV**: For direct ERP import
- **Excel**: Full data with nutritional info

---

## ☁️ Deploy to Streamlit Cloud

Deploy your own instance for free:

### Step 1: Push to GitHub
Push your code to a GitHub repository.

### Step 2: Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Select your repository
4. Set the main file as `app.py`

### Step 3: Add Secrets
In Streamlit Cloud settings, add your API key:

```
GEMINI_API_KEY = "your_api_key_here"
```

### Step 4: Deploy
Your app will be live at `https://your-app-name.streamlit.app`

---

## 📂 Project Structure

```
foodscanner-erp/
├── app.py                 # Streamlit web interface
├── main.py                # CLI version (original)
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── modules/
│   ├── ocr.py           # Gemini OCR processing
│   ├── api_client.py    # Open Food Facts client
│   └── data_handler.py  # Data processing & export
├── utils/
│   ├── logger.py
│   └── progress.py
└── images/               # Input images (local)
```

---

## 🛠️ Technologies

- **Python 3.10+**
- **Streamlit** - Web UI framework
- **Google Gemini Flash 2.0** - OCR for text extraction
- **Open Food Facts API** - Product database
- **Pandas** - Data handling
- **OpenPyXL** - Excel export

---

## 📝 License

This project is licensed under the **MIT License** - feel free to use, modify, and distribute.

---

## 🤝 Contributing

Contributions are welcome! Whether you want to:

- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

**Join us in making inventory management easier for everyone!**

---

## ⚠️ Notes

- **API Keys**: Gemini API has a free tier. Check [Google AI Studio](https://aistudio.google.com/app/apikey) for limits.
- **Privacy**: Images are processed in memory and not stored on servers.
- **Data Accuracy**: Always verify the generated grid before importing to your ERP. Open Food Facts depends on community-contributed data.

---

## 🏷️ Tags

`#OpenSource` `#ERP` `#Inventory` `#Streamlit` `#Python` `#Supermarket` `#OCR` `#FoodData`

---

## 📚 Documentation / Documentación

- [English](README.md)
- [Español](README.es.md)

---

> **Made with 💚 by [Dolan](https://github.com/nashishoo) | [Catapaz](https://www.catapaz.site)**
> 
> *Simplifying inventory management, one photo at a time.*
