#!/usr/bin/env python3
"""
Food Scanner - Streamlit Web Interface
Interfaz visual para escanear productos alimenticios
"""
import os
import sys
from pathlib import Path
import tempfile
import shutil

import streamlit as st
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from modules import OCRProcessor, OpenFoodFactsClient, DataHandler

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FoodScanner - ERP",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'images_uploaded' not in st.session_state:
        st.session_state.images_uploaded = []
    if 'data_handler' not in st.session_state:
        st.session_state.data_handler = DataHandler()


def process_images(uploaded_files, demo_mode=False, api_key=None):
    """
    Process uploaded images and extract product data.
    
    Args:
        uploaded_files: List of uploaded file objects
        demo_mode: Whether to use demo mode (no API key required)
        api_key: Gemini API key for OCR
    
    Returns:
        List of processed results
    """
    results = []
    data_handler = DataHandler()
    
    # Create temporary directory for images
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        # Save uploaded files to temp directory
        image_paths = []
        for uploaded_file in uploaded_files:
            temp_path = temp_dir / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            image_paths.append(temp_path)
        
        # Initialize OCR processor
        try:
            ocr_processor = OCRProcessor(api_key=api_key if api_key else None, demo_mode=demo_mode)
        except ValueError as e:
            st.error(f"Error de configuración: {str(e)}")
            return []
        
        # Initialize API client
        api_client = OpenFoodFactsClient()
        
        # Process each image
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, image_path in enumerate(image_paths):
            status_text.text(f"Procesando imagen {idx + 1}/{len(image_paths)}: {image_path.name}")
            
            # OCR - Extract product names
            product_list = ocr_processor.process_image(image_path)
            
            if not product_list or product_list == ["ERROR"]:
                data_handler.add_result_with_source(
                    image_path.name, 
                    "ERROR_OCR", 
                    None
                )
                continue
            
            if product_list == ["NO_DETECTADO"]:
                data_handler.add_result_with_source(
                    image_path.name,
                    "NO_DETECTADO",
                    None
                )
                continue
            
            # Search each product in Open Food Facts
            for product_name in product_list:
                product_data = api_client.search_product(product_name)
                data_handler.add_result_with_source(
                    image_path.name,
                    product_name,
                    product_data
                )
            
            progress_bar.progress((idx + 1) / len(image_paths))
        
        status_text.text("¡Procesamiento completado!")
        api_client.close()
        
        return data_handler.results
        
    except Exception as e:
        st.error(f"Error durante el procesamiento: {str(e)}")
        return []
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def display_erp_grid(results):
    """
    Display results in ERP grid format.
    
    Args:
        results: List of result dictionaries
    """
    if not results:
        st.info("No hay resultados para mostrar")
        return
    
    # Create DataFrame
    import pandas as pd
    df = pd.DataFrame(results)
    
    # ERP Column order for display
    erp_columns = ["nombre", "categoria", "proveedor", "detalle", "codigo_barra"]
    
    # Filter to only ERP columns that exist
    display_cols = [col for col in erp_columns if col in df.columns]
    
    # Add extra columns if they exist
    extra_cols = ["producto_detectado", "estado", "marca", "imagen"]
    for col in extra_cols:
        if col in df.columns and col not in display_cols:
            display_cols.append(col)
    
    # Create editable dataframe for ERP
    st.subheader("📋 Grilla ERP -Editable-")
    
    # Display with editing capability
    edited_df = st.data_editor(
        df[display_cols],
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "categoria": st.column_config.SelectboxColumn(
                "Categoría",
                options=["bebestible", "comida", "helado", "fiambre", "lacteo", ""],
                required=False
            ),
            "proveedor": st.column_config.TextColumn(
                "Proveedor",
                help="Ej: Nestle, Evercrisp, Walmart, Soprole"
            ),
            "detalle": st.column_config.TextColumn(
                "Detalle",
                help="Gramaje o volumen (ej: 500g, 1L)"
            ),
            "codigo_barra": st.column_config.TextColumn(
                "Código de Barra",
                help="Código de barras del producto"
            )
        }
    )
    
    # Store edited data back
    st.session_state.edited_results = edited_df


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Header
    st.title("🛒 FoodScanner - ERP")
    st.markdown("### Escanea productos de supermercado y genera tu grilla para ERP")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # API Key input
        api_key = st.text_input(
            "API Key de Gemini",
            type="password",
            help="Necesaria para OCR. También puedes usar variable GEMINI_API_KEY o .env"
        )
        
        # Demo mode toggle
        demo_mode = st.toggle(
            "Modo Demo",
            value=False,
            help="Usa datos simulados sin necesidad de API key"
        )
        
        st.divider()
        
        st.header("ℹ️ Acerca de")
        st.markdown("""
        **FoodScanner ERP** extrae productos de imágenes de gondolas de supermercado 
        y los busca en Open Food Facts para obtener datos nutricionales.
        
        ### Formatos soportados:
        - JPG, JPEG, PNG, WebP, BMP
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Subir Imágenes")
        uploaded_files = st.file_uploader(
            "Arrastra imágenes de productos o haz clic para seleccionar",
            type=["jpg", "jpeg", "png", "webp", "bmp"],
            accept_multiple_files=True,
            help="Puedes subir varias imágenes a la vez"
        )
    
    # Process button
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} imagen(es) cargada(s)")
        
        if st.button("🔍 Procesar Imágenes", type="primary", disabled=st.session_state.processing):
            st.session_state.processing = True
            
            with st.spinner("Procesando imágenes..."):
                results = process_images(uploaded_files, demo_mode=demo_mode, api_key=api_key if api_key else None)
                st.session_state.results = results
            
            st.session_state.processing = False
    
    # Display results
    if st.session_state.results:
        st.divider()
        
        # Summary
        summary = {
            "total": len(st.session_state.results),
            "encontrados": sum(1 for r in st.session_state.results if r.get("estado") == "ENCONTRADO"),
            "no_encontrados": sum(1 for r in st.session_state.results if r.get("estado") == "NO_ENCONTRADO"),
        }
        
        # Summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Productos", summary["total"])
        m2.metric("✅ Encontrados", summary["encontrados"])
        m3.metric("❌ No Encontrados", summary["no_encontrados"])
        tasa = (summary["encontrados"] / summary["total"] * 100) if summary["total"] > 0 else 0
        m4.metric("Tasa de Éxito", f"{tasa:.1f}%")
        
        # Display ERP grid
        display_erp_grid(st.session_state.results)
        
        # Export section
        st.divider()
        st.subheader("💾 Exportar")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            # Export to Excel (full data)
            import pandas as pd
            df_full = pd.DataFrame(st.session_state.results)
            
            # Reorder columns - ERP fields first
            erp_cols = ["nombre", "categoria", "proveedor", "detalle", "codigo_barra"]
            other_cols = [c for c in df_full.columns if c not in erp_cols]
            df_export = df_full[erp_cols + other_cols]
            
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV (para ERP)",
                data=csv,
                file_name="foodscan_erp.csv",
                mime="text/csv",
                type="primary"
            )
        
        with col_exp2:
            # Export full Excel using BytesIO
            from io import BytesIO
            excel_buffer = BytesIO()
            df_full.to_excel(excel_buffer, sheet_name="Productos", index=False, engine="openpyxl")
            excel_data = excel_buffer.getvalue()
            
            st.download_button(
                label="📊 Descargar Excel (completo)",
                data=excel_data,
                file_name="foodscan_completo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


def add_footer():
    """Add footer with credits."""
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: gray; padding: 20px;">
            <p>Desarrollado por 
                <a href="https://github.com/nashishoo" target="_blank">Dolan</a> | 
                <a href="https://www.catapaz.site" target="_blank">Catapaz</a>
            </p>
            <p style="font-size: 12px;">© 2026 FoodScanner ERP - Herramienta de código abierto</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
    add_footer()
