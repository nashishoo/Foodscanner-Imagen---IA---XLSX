"""
Food Scanner - Data Handler Module
Handles data processing and Excel export using Pandas
"""
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

import config

logger = logging.getLogger(__name__)


class DataHandler:
    """Handles data processing and Excel export operations."""
    
    def __init__(self):
        """Initialize the data handler."""
        self.results = []
        logger.info("Data Handler inicializado")
    
    def _extract_category_from_openfood(self, categories: str) -> str:
        """
        Extract the main category from Open Food Facts categories string.
        Maps to ERP categories: bebestible, comida, helado, fiambre, lacteo, etc.
        """
        if not categories:
            return ""
        
        categories_lower = categories.lower()
        
        # Category mapping from Open Food Facts to ERP categories
        category_mappings = {
            "bebestible": ["bebida", "bebida", "drink", "beverage", "agua", "jugo", "zumo", "jugu", "refresco", "soda", "cerveza", "vino", "licor", "cafe", "te", "leche"],
            "helado": ["helado", "ice cream", "ice-cream", "gelato", "sorbete"],
            "fiambre": ["fiambre", "jamón", "jam", "embutido", "salchicha", "chorizo", "tocino", "bacon", "paté"],
            "lacteo": ["leche", "yogur", "yogurt", "queso", "cheese", "mantequilla", "crema", "nata", "kumis", "kumys"],
            "comida": ["comida", "food", "pasta", "arroz", "cereal", "galleta", "biscuit", "pan", "bread", "dulce", "confitería", "chocolate", "carne", "pescado", "verdura", "vegetal", "fruta", "sopa", "salsas"]
        }
        
        for erp_category, keywords in category_mappings.items():
            for keyword in keywords:
                if keyword in categories_lower:
                    return erp_category
        
        return "comida"  # Default
    
    def _extract_quantity_from_openfood(self, product_data: dict) -> str:
        """
        Extract quantity details from Open Food Facts product data.
        Returns formatted string like "500g", "1L", "200ml", etc.
        """
        quantity = product_data.get("quantity", "")
        serving_size = product_data.get("serving_size", "")
        
        if quantity:
            return str(quantity)
        elif serving_size:
            return str(serving_size)
        else:
            # Try to extract from other fields
            product_name = product_data.get("product_name", "")
            # Common patterns
            import re
            patterns = [
                r'(\d+[.,]?\d*)\s*(g|gramos|ml|mililitros|l|litros|kg|kilogramos)',
                r'(\d+[.,]?\d*)\s*(u|unidades|pcs|pieces)'
            ]
            for pattern in patterns:
                match = re.search(pattern, product_name.lower())
                if match:
                    return f"{match.group(1)}{match.group(2)}"
        
        return ""
    
    def _extract_brand_as_proveedor(self, brands: str) -> str:
        """
        Extract and normalize brand name as supplier (proveedor).
        """
        if not brands:
            return ""
        
        # Brands can be comma-separated, take the first one
        brand_list = [b.strip() for b in brands.split(",")]
        return brand_list[0] if brand_list else ""
    
    def add_result(
        self,
        image_name: str,
        product_name: str,
        product_data: Optional[dict] = None
    ):
        """
        Add a scan result to the collection.
        
        Args:
            image_name: Name of the source image
            product_name: Extracted product name from OCR
            product_data: Nutritional data from API (optional)
        """
        result = {
            "imagen": image_name,
            "producto_detectado": product_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        # Add product data if available
        if product_data:
            # Get raw data
            raw_categories = product_data.get("categories", "")
            raw_brands = product_data.get("brands", "")
            
            # Extract ERP-specific fields
            categoria = self._extract_category_from_openfood(raw_categories)
            proveedor = self._extract_brand_as_proveedor(raw_brands)
            detalle = self._extract_quantity_from_openfood(product_data)
            codigo_barra = product_data.get("code", "")
            
            result.update({
                # ERP Grilla Fields
                "nombre": product_name,
                "categoria": categoria,
                "proveedor": proveedor,
                "detalle": detalle,
                "codigo_barra": codigo_barra,
                # Original fields for reference
                "codigo": codigo_barra,
                "marca": raw_brands,
                "categorias": raw_categories,
                "nutrition_grade": product_data.get("nutrition_grade", ""),
                # Energy
                "energia_kcal_100g": product_data.get("energy_kcal_100g", 0),
                "energia_kj_100g": product_data.get("energy_kj_100g", 0),
                # Macros
                "grasas_100g": product_data.get("fat_100g", 0),
                "grasas_saturadas_100g": product_data.get("saturated_fat_100g", 0),
                "carbohidratos_100g": product_data.get("carbohydrates_100g", 0),
                "azucares_100g": product_data.get("sugars_100g", 0),
                "fibra_100g": product_data.get("fiber_100g", 0),
                "proteinas_100g": product_data.get("proteins_100g", 0),
                "sal_100g": product_data.get("salt_100g", 0),
                "sodio_100g": product_data.get("sodium_100g", 0),
                "estado": "ENCONTRADO"
            })
        else:
            # No product data available - leave ERP fields empty
            result.update({
                # ERP Grilla Fields
                "nombre": product_name,
                "categoria": "",
                "proveedor": "",
                "detalle": "",
                "codigo_barra": "",
                # Original fields
                "codigo": "",
                "marca": "",
                "categorias": "",
                "nutrition_grade": "",
                "energia_kcal_100g": 0,
                "energia_kj_100g": 0,
                "grasas_100g": 0,
                "grasas_saturadas_100g": 0,
                "carbohidratos_100g": 0,
                "azucares_100g": 0,
                "fibra_100g": 0,
                "proteinas_100g": 0,
                "sal_100g": 0,
                "sodio_100g": 0,
                "estado": "NO_ENCONTRADO" if product_name != "ERROR" else "ERROR_OCR"
            })
        
        self.results.append(result)
        logger.debug("Resultado añadido: %s - %s", image_name, product_name)
    
    def add_result_with_source(
        self,
        image_name: str,
        product_name: str,
        product_data: Optional[dict] = None
    ):
        """
        Add a scan result with image source (alias for add_result).
        
        Args:
            image_name: Name of the source image
            product_name: Extracted product name from OCR
            product_data: Nutritional data from API (optional)
        """
        # Use the same logic as add_result
        self.add_result(image_name, product_name, product_data)
    
    def export_to_excel(self, output_path: Path) -> bool:
        """
        Export results to an Excel file.
        
        Args:
            output_path: Path for the output Excel file
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if not self.results:
                logger.warning("No hay resultados para exportar")
                return False
            
            # Create DataFrame
            df = pd.DataFrame(self.results)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export to Excel with formatting
            with pd.ExcelWriter(
                output_path,
                engine="openpyxl"
            ) as writer:
                df.to_excel(
                    writer,
                    sheet_name=config.EXCEL_SHEET_NAME,
                    index=False
                )
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets[config.EXCEL_SHEET_NAME]
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info("Resultados exportados a: %s", output_path)
            return True
            
        except Exception as e:
            logger.error("Error exportando a Excel: %s", str(e))
            return False
    
    def get_summary(self) -> dict:
        """
        Get a summary of scan results.
        
        Returns:
            Dictionary with summary statistics
        """
        total = len(self.results)
        found = sum(1 for r in self.results if r.get("estado") == "ENCONTRADO")
        not_found = sum(1 for r in self.results if r.get("estado") == "NO_ENCONTRADO")
        errors = sum(1 for r in self.results if r.get("estado") == "ERROR_OCR")
        
        return {
            "total": total,
            "encontrados": found,
            "no_encontrados": not_found,
            "errores_ocr": errors,
            "tasa_exito": (found / total * 100) if total > 0 else 0
        }
    
    def clear(self):
        """Clear all stored results."""
        self.results.clear()
        logger.debug("Resultados清除")
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get results as a Pandas DataFrame.
        
        Returns:
            DataFrame containing all results
        """
        return pd.DataFrame(self.results)
