"""
Food Scanner - OCR Module
Uses Gemini Flash 2.0 for text extraction from product images
"""
import logging
from pathlib import Path
from typing import Optional

try:
    import google.genai as genai
    USE_NEW_PACKAGE = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_PACKAGE = False

from PIL import Image

import config

logger = logging.getLogger(__name__)


class OCRProcessor:
    """Processes product images using Gemini to extract product names."""
    
    def __init__(self, api_key: Optional[str] = None, demo_mode: bool = False):
        """
        Initialize the OCR processor.
        
        Args:
            api_key: Gemini API key. If not provided, uses config.GEMINI_API_KEY
            demo_mode: If True, uses mock data for testing
        """
        self.demo_mode = demo_mode
        self.api_key = api_key or config.GEMINI_API_KEY
        
        if demo_mode:
            logger.info("OCR Processor inicializado en MODO DEMO")
            return
        
        if not self.api_key:
            raise ValueError(
                "API key no proporcionada. Usa --api-key o crea un archivo .env con GEMINI_API_KEY"
            )
        
        # Configure Gemini
        if USE_NEW_PACKAGE:
            self.client = genai.Client(api_key=self.api_key)
        else:
            genai.configure(api_key=self.api_key)
        
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        
        logger.info("OCR Processor inicializado con modelo %s", config.GEMINI_MODEL)
    
    def process_image(self, image_path: Path) -> list:
        """
        Process a single image and extract ALL product names.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of extracted product names or ["NO_DETECTADO"] if extraction fails
        """
        # Demo mode - return mock data
        if self.demo_mode:
            logger.info("Procesando imagen (DEMO): %s", image_path.name)
            mock_products = ["Leche Entera", "Galletas Maria", "Jugo de Naranja", "Yogur Natural", "Pasta de Dientes"]
            import random
            # Return 3-5 random products for demo
            num_products = random.randint(3, 5)
            selected = random.sample(mock_products, min(num_products, len(mock_products)))
            logger.info("Productos detectados (DEMO): %s", selected)
            return selected
        
        try:
            logger.info("Procesando imagen: %s", image_path.name)
            
            # Load and validate image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Generate content with Gemini
            if USE_NEW_PACKAGE:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[config.OCR_PROMPT, image]
                )
            else:
                response = self.model.generate_content(
                    [
                        config.OCR_PROMPT,
                        image
                    ],
                    generation_config={
                        "max_output_tokens": config.GEMINI_MAX_TOKENS,
                        "temperature": config.GEMINI_TEMPERATURE,
                    }
                )
            
            # Extract text from response
            text_response = response.text.strip()
            
            # Handle "NO_DETECTADO" case
            if text_response.upper() == "NO_DETECTADO":
                logger.warning("No se detectaron productos en: %s", image_path.name)
                return ["NO_DETECTADO"]
            
            # Parse comma-separated list
            products = [p.strip() for p in text_response.split(',') if p.strip()]
            
            if products:
                logger.info("Productos detectados: %s", products)
            else:
                logger.warning("No se pudieron parsear productos de: %s", image_path.name)
                return ["NO_DETECTADO"]
            
            return products
            
        except Exception as e:
            logger.error("Error procesando imagen %s: %s", image_path.name, str(e))
            return ["ERROR"]
    
    def process_batch(self, image_paths: list[Path]) -> dict[Path, str]:
        """
        Process multiple images and return a dictionary of results.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            Dictionary mapping image paths to extracted product names
        """
        results = {}
        
        for image_path in image_paths:
            results[image_path] = self.process_image(image_path)
        
        return results
    
    @staticmethod
    def is_valid_image(file_path: Path) -> bool:
        """
        Check if a file is a valid image.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists and has valid image extension
        """
        if not file_path.exists():
            return False
        
        return file_path.suffix.lower() in config.SUPPORTED_IMAGE_EXTENSIONS
    
    @staticmethod
    def get_images_from_folder(folder_path: Path) -> list[Path]:
        """
        Get all valid images from a folder.
        
        Args:
            folder_path: Path to the folder containing images
            
        Returns:
            List of paths to valid image files
        """
        if not folder_path.exists() or not folder_path.is_dir():
            logger.error("Carpeta no encontrada: %s", folder_path)
            return []
        
        images = []
        for file_path in folder_path.iterdir():
            if file_path.is_file() and OCRProcessor.is_valid_image(file_path):
                images.append(file_path)
        
        logger.info("Encontradas %d imágenes en %s", len(images), folder_path)
        return sorted(images)
