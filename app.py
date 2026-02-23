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
        # Save uploaded files to temp directory and session state
        image_paths = []
        if 'uploaded_images_dict' not in st.session_state:
            st.session_state.uploaded_images_dict = {}
            
        for uploaded_file in uploaded_files:
            # Save raw bytes to session state for later visualization
            file_bytes = uploaded_file.getvalue()
            st.session_state.uploaded_images_dict[uploaded_file.name] = file_bytes
            
            temp_path = temp_dir / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(file_bytes)
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
            
            # OCR - Extract product names (now returns list of dicts)
            product_list = ocr_processor.process_image(image_path)
            
            # Handle empty or error cases
            if not product_list:
                continue
                
            first_prod_name = product_list[0].get("nombre", "") if isinstance(product_list[0], dict) else str(product_list[0])
            
            if first_prod_name == "ERROR" or product_list[0] == "ERROR":
                err_msg = product_list[0].get("error", "Error desconocido") if isinstance(product_list[0], dict) else "Error procesando imagen"
                st.error(f"Error procesando {image_path.name}: {err_msg}")
                data_handler.add_result_with_source(
                    image_path.name, 
                    {"nombre": "ERROR", "detalle": err_msg}, 
                    None
                )
                continue
            
            if first_prod_name == "NO_DETECTADO":
                data_handler.add_result_with_source(
                    image_path.name,
                    {"nombre": "NO_DETECTADO"},
                    None
                )
                continue
            
            # Search each product in Open Food Facts
            for product_dict in product_list:
                product_name = product_dict.get("nombre", "")
                if product_name:
                    product_data = api_client.search_product(product_name)
                    data_handler.add_result_with_source(
                        image_path.name,
                        product_dict,
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
    
    # Add 'Seleccionar' column for selection
    if "Seleccionar" not in df.columns:
        df.insert(0, "Seleccionar", False)
        
    # ERP Column order for display EXACTAMENTE COMO SE SOLICITÓ
    erp_columns = ["Seleccionar", "nombre", "codigoBarras", "detalle", "cantidad", "imagen", "precioCompra", "precioVenta", "stock", "stockMinimo", "proveedor", "categoria", "fechaVencimiento"]
    
    st.subheader("📋 Grilla ERP -Editable-")
    st.markdown("*Marca la casilla 'Seleccionar' para ver la imagen de origen.*")
    
    # Create two columns for Split View (Grid 70%, Image 30%)
    grid_col, img_col = st.columns([7, 3])
    
    with grid_col:
        # Display with editing capability and selection enabled
        edited_df = st.data_editor(
            df[erp_columns],
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="erp_grid",
            column_config={
                "Seleccionar": st.column_config.CheckboxColumn("Seleccionar", help="Marca para ver la imagen"),
                "nombre": st.column_config.TextColumn("Nombre"),
                "codigoBarras": st.column_config.TextColumn("Código de Barras"),
                "detalle": st.column_config.TextColumn("Detalle (Peso/Vol)"),
                "cantidad": st.column_config.NumberColumn("Cantidad", min_value=1, step=1, default=1),
                "imagen": st.column_config.TextColumn("Imagen Origen", disabled=True),
                "precioCompra": st.column_config.NumberColumn("Precio Compra", format="$%d"),
                "precioVenta": st.column_config.NumberColumn("Precio Venta", format="$%d"),
                "stock": st.column_config.NumberColumn("Stock", step=1),
                "stockMinimo": st.column_config.NumberColumn("Stock Mínimo", step=1),
                "proveedor": st.column_config.TextColumn("Proveedor/Marca"),
                "categoria": st.column_config.TextColumn("Categoría"),
                "fechaVencimiento": st.column_config.DateColumn("Fecha Vencimiento", format="DD/MM/YYYY")
            }
        )
        # Store edited data back
        st.session_state.edited_results = edited_df
        
    with img_col:
        # Logic to display image on selection
        st.markdown("### 🖼️ Evidencia Visual")
        
        # Get selected rows
        selected_rows = edited_df[edited_df["Seleccionar"] == True]
        
        if not selected_rows.empty:
            # Get the first selected row
            first_selected = selected_rows.iloc[0]
            selected_image_name = first_selected["imagen"]
            st.info(f"Mostrando: **{selected_image_name}**")
            
            # Retrieve from session_state
            if "uploaded_images_dict" in st.session_state and selected_image_name in st.session_state.uploaded_images_dict:
                st.image(
                    st.session_state.uploaded_images_dict[selected_image_name], 
                    use_container_width=True,
                    caption=f"Producto referenciado: {first_selected['nombre']}"
                )
            else:
                st.warning("Imagen no encontrada en memoria. Re-sube las fotos.")
        else:
            st.info("👈 Marca la casilla 'Seleccionar' en la grilla para verificar su imagen de origen.")


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
            
            # Reorder columns - EXACTAMENTE COMO SE SOLICITÓ
            erp_cols = ["nombre", "codigoBarras", "detalle", "cantidad", "imagen", "precioCompra", "precioVenta", "stock", "stockMinimo", "proveedor", "categoria", "fechaVencimiento"]
            # To export edits, use the edited_df that was saved in session_state, OR standard results if not edited
            
            df_export = st.session_state.edited_results if "edited_results" in st.session_state else pd.DataFrame(st.session_state.results)[erp_cols]
            
            if "Seleccionar" in df_export.columns:
                df_export = df_export.drop(columns=["Seleccionar"])
            
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="foodscan_erp.csv",
                mime="text/csv",
                type="primary"
            )
        
        with col_exp2:
            # Export full Excel using BytesIO
            from io import BytesIO
            excel_buffer = BytesIO()
            df_export.to_excel(excel_buffer, sheet_name="Productos", index=False, engine="openpyxl")
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
