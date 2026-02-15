"""
Food Scanner - API Client Module
Handles communication with Open Food Facts API
"""
import logging
from typing import Optional
import requests

import config

logger = logging.getLogger(__name__)


class OpenFoodFactsClient:
    """Client for interacting with the Open Food Facts API."""
    
    def __init__(self):
        """Initialize the API client with configuration."""
        self.base_url = config.OPEN_FOOD_FACTS_BASE_URL
        self.search_endpoint = config.OPEN_FOOD_FACTS_SEARCH_ENDPOINT
        self.product_endpoint = config.OPEN_FOOD_FACTS_PRODUCT_ENDPOINT
        self.user_agent = config.OPEN_FOOD_FACTS_USER_AGENT
        
        # Setup session with headers
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent
        })
        
        logger.info("Open Food Facts API Client inicializado")
    
    def search_product(self, product_name: str) -> Optional[dict]:
        """
        Search for a product by name.
        
        Args:
            product_name: Name of the product to search for
            
        Returns:
            Product data dictionary or None if not found
        """
        try:
            logger.info("Buscando producto: %s", product_name)
            
            # Build search URL
            search_url = f"{self.base_url}{self.search_endpoint}"
            
            # Search parameters
            params = {
                "search_terms": product_name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 5,
                "fields": "code,product_name,nutriments,brands,categories,quantity,serving_size"
            }
            
            # Make request
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if products found
            products = data.get("products", [])
            if not products:
                logger.warning("No se encontraron productos para: %s", product_name)
                return None
            
            # Return first match
            product = products[0]
            logger.info("Producto encontrado: %s", product.get("product_name", "Unknown"))
            
            return self._parse_product_data(product)
            
        except requests.exceptions.RequestException as e:
            logger.error("Error en la búsqueda de %s: %s", product_name, str(e))
            return None
        except Exception as e:
            logger.error("Error inesperado buscando %s: %s", product_name, str(e))
            return None
    
    def get_product_by_barcode(self, barcode: str) -> Optional[dict]:
        """
        Get product information by barcode.
        
        Args:
            barcode: Product barcode (EAN-13, UPC, etc.)
            
        Returns:
            Product data dictionary or None if not found
        """
        try:
            logger.info("Consultando barcode: %s", barcode)
            
            # Build API URL
            api_url = f"{self.base_url}{self.product_endpoint}/{barcode}.json"
            
            # Make request
            response = self.session.get(api_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if product found
            if data.get("status") != 1:
                logger.warning("Producto no encontrado para barcode: %s", barcode)
                return None
            
            product = data.get("product", {})
            return self._parse_product_data(product)
            
        except requests.exceptions.RequestException as e:
            logger.error("Error consultando barcode %s: %s", barcode, str(e))
            return None
        except Exception as e:
            logger.error("Error inesperado consultando %s: %s", barcode, str(e))
            return None
    
    def _parse_product_data(self, product: dict) -> dict:
        """
        Parse and normalize product data from API response.
        
        Args:
            product: Raw product data from API
            
        Returns:
            Normalized product dictionary
        """
        nutriments = product.get("nutriments", {})
        
        # Extract nutritional values (per 100g)
        parsed = {
            "code": product.get("code", ""),
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", ""),
            "categories": product.get("categories", ""),
            "quantity": product.get("quantity", ""),
            "serving_size": product.get("serving_size", ""),
            # Energy
            "energy_kcal_100g": nutriments.get("energy-kcal_100g", 0),
            "energy_kj_100g": nutriments.get("energy-kj_100g", 0),
            # Macros
            "fat_100g": nutriments.get("fat_100g", 0),
            "saturated_fat_100g": nutriments.get("saturated-fat_100g", 0),
            "carbohydrates_100g": nutriments.get("carbohydrates_100g", 0),
            "sugars_100g": nutriments.get("sugars_100g", 0),
            "fiber_100g": nutriments.get("fiber_100g", 0),
            "proteins_100g": nutriments.get("proteins_100g", 0),
            "salt_100g": nutriments.get("salt_100g", 0),
            "sodium_100g": nutriments.get("sodium_100g", 0),
            # Additional
            "nutrition_grade": product.get("nutrition-grades", ""),
        }
        
        return parsed
    
    def close(self):
        """Close the session."""
        self.session.close()
        logger.debug("Sesión API cerrada")
