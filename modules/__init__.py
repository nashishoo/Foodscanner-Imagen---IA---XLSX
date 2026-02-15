"""
Food Scanner - Modules Package
Contains OCR, API client, and data handler modules
"""
from .ocr import OCRProcessor
from .api_client import OpenFoodFactsClient
from .data_handler import DataHandler

__all__ = ["OCRProcessor", "OpenFoodFactsClient", "DataHandler"]
