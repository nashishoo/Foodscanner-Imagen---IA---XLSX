#!/usr/bin/env python3
"""
Food Scanner - Main CLI Application
Analiza imágenes de productos alimenticios y extrae información nutricional
"""
import argparse
import sys
from pathlib import Path

import config
from modules import OCRProcessor, OpenFoodFactsClient, DataHandler
from utils import setup_logger


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Food Scanner - Analiza imágenes de productos alimenticios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --input images/
  python main.py --input images/ --output resultados.xlsx
  python main.py --input images/ --api-key TU_API_KEY --verbose
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="Carpeta con las imágenes de productos a analizar"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=str(config.DEFAULT_OUTPUT_FILE),
        help=f"Archivo Excel de salida (default: {config.DEFAULT_OUTPUT_FILE})"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API key de Gemini (también puede usar variable GEMINI_API_KEY o archivo .env)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Modo verbose (muestra mensajes de debug)"
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Modo demo: usa datos simulados sin necesidad de API key"
    )
    
    return parser.parse_args()


def main():
    """Main application entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logger(verbose=args.verbose)
    logger.info("=" * 60)
    logger.info("Food Scanner - Inicio del proceso")
    logger.info("=" * 60)
    
    # Validate input path
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Carpeta de entrada no encontrada: {input_path}")
        sys.exit(1)
    
    if not input_path.is_dir():
        logger.error(f"La ruta de entrada debe ser una carpeta: {input_path}")
        sys.exit(1)
    
    # Validate output path
    output_path = Path(args.output)
    
    try:
        # Initialize components
        logger.info("Inicializando componentes...")
        
        # OCR Processor
        try:
            ocr_processor = OCRProcessor(api_key=args.api_key, demo_mode=args.demo)
        except ValueError as e:
            logger.error(str(e))
            logger.error("Por favor, proporciona una API key usando --api-key, crea un archivo .env, o usa --demo")
            sys.exit(1)
        
        # API Client
        api_client = OpenFoodFactsClient()
        
        # Data Handler
        data_handler = DataHandler()
        
        # Get images from folder
        logger.info(f"Buscando imágenes en: {input_path}")
        images = OCRProcessor.get_images_from_folder(input_path)
        
        if not images:
            logger.warning("No se encontraron imágenes en la carpeta especificada")
            logger.info(f"Formatos soportados: {', '.join(config.SUPPORTED_IMAGE_EXTENSIONS)}")
            sys.exit(0)
        
        logger.info(f"Comenzando análisis de {len(images)} imágenes...")
        
        # Track total products for progress
        total_products = 0
        
        # First pass: get all products from all images
        logger.info("")
        logger.info("=== FASE 1: Extrayendo productos de imágenes ===")
        
        all_products = []  # List of (image_path, product_name)
        
        for image_path in images:
            logger.info("")
            logger.info("-" * 50)
            logger.info(f"Procesando imagen: {image_path.name}")
            
            # Step 1: OCR - Extract product NAMES (list)
            product_list = ocr_processor.process_image(image_path)
            
            if not product_list or product_list == ["ERROR"]:
                logger.error(f"Error en OCR para {image_path.name}")
                continue
            
            if product_list == ["NO_DETECTADO"]:
                logger.warning(f"No se detectaron productos en {image_path.name}")
                continue
            
            # Add each product with its image source
            for product_name in product_list:
                all_products.append((image_path.name, product_name))
                total_products += 1
            
            logger.info(f"  -> {len(product_list)} productos detectados")
        
        logger.info("")
        logger.info(f"Total productos detectados: {len(all_products)}")
        
        if not all_products:
            logger.warning("No se detectaron productos en ninguna imagen")
            sys.exit(0)
        
        # Second pass: search each product in Open Food Facts
        logger.info("")
        logger.info("=== FASE 2: Buscando en Open Food Facts ===")
        
        for idx, (image_name, product_name) in enumerate(all_products, 1):
            logger.info("")
            logger.info(f"[{idx}/{len(all_products)}] Producto: {product_name}")
            
            # Search in Open Food Facts
            product_data = api_client.search_product(product_name)
            
            # Add result with image origin
            data_handler.add_result_with_source(image_name, product_name, product_data)
            
            if product_data:
                logger.info(f"  [OK] Encontrado: {product_data.get('product_name', 'N/A')}")
                logger.info(f"      Energia: {product_data.get('energy_kcal_100g', 0)} kcal/100g")
            else:
                logger.warning(f"  [X] No encontrado en base de datos")
        
        # Export results
        logger.info("")
        logger.info("=" * 60)
        logger.info("Exportando resultados...")
        
        if data_handler.export_to_excel(output_path):
            logger.info(f"[OK] Resultados guardados en: {output_path}")
        else:
            logger.error("Error al exportar resultados")
            sys.exit(1)
        
        # Print summary
        summary = data_handler.get_summary()
        logger.info("")
        logger.info("-" * 50)
        logger.info("RESUMEN")
        logger.info("-" * 50)
        logger.info(f"Total de imágenes procesadas: {summary['total']}")
        logger.info(f"Productos encontrados: {summary['encontrados']}")
        logger.info(f"Productos no encontrados: {summary['no_encontrados']}")
        logger.info(f"Errores OCR: {summary['errores_ocr']}")
        logger.info(f"Tasa de exito: {summary['tasa_exito']:.1f}%")
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("Food Scanner - Proceso completado")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.warning("\nProceso interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup
        if 'api_client' in locals():
            api_client.close()


if __name__ == "__main__":
    main()
