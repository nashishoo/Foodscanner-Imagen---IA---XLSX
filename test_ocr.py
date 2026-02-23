import os
import sys
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.ocr import OCRProcessor

def test():
    load_dotenv()
    image_path = Path("images/gondola .png")
    
    try:
        processor = OCRProcessor()
        print("Model initialized")
        
        # We might want to bypass the try/except in process_image to get the REAL stacktrace, 
        # but let's just see if process_image logs anything to stdout.
        # process_image uses logger, so let's configure logging to stdout
        import logging
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        
        results = processor.process_image(image_path)
        print("RESULTS:", results)
        
    except Exception as e:
        print("ERROR:")
        traceback.print_exc()

if __name__ == "__main__":
    test()
