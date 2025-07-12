import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pytesseract
from PIL import Image
import re
from config.settings import SUPPORTED_LANGUAGES, EXCLUDED_MENU_HEADERS, MIN_DISH_NAME_LENGTH, MAX_DISH_NAME_LENGTH

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract\tesseract.exe'


class OCRService:
    """Extracts dish names from menu images using OCR"""

    def __init__(self):
        pass

    def extract_text(self, image: Image.Image) -> str:
        """Runs OCR on image and returns raw text"""
        return pytesseract.image_to_string(image, lang=SUPPORTED_LANGUAGES)

    def extract_dish_names(self, text: str) -> list:
        """Cleans OCR text and returns a list of potential dish names"""
        lines = text.split('\n')
        cleaned = []

        for line in lines:
            dish = line.strip()

            
            if len(dish) < MIN_DISH_NAME_LENGTH or len(dish) > MAX_DISH_NAME_LENGTH:
                continue

            
            if any(excluded.lower() in dish.lower() for excluded in EXCLUDED_MENU_HEADERS):
                continue

            
            dish = re.sub(r'\d+[\.,]?\d*\s*(AZN|azn|₼)?', '', dish).strip()

            if dish and dish not in cleaned:
                cleaned.append(dish)

        return cleaned
