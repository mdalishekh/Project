import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from chat.configuration.config import *

# Tesseract path for Docker
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def ocr_image(image_path):
    try:
        logging.info("Image ocr performing")
        with Image.open(image_path) as image:
            text = pytesseract.image_to_string(image)
        if text:
            print(text)
            return text
        return None
            # with open("text_file_path","w") as file:
            #     file.write(text) 
    except Exception as error:
        logging.error(f"Error occurred while performing OCR: {str(error)}")
        
def ocr_pdf(pdf_path):
    logging.info("PDF ocr performing")
    text = ''
    images = convert_from_path(pdf_path)
    for img in images:
        text += pytesseract.image_to_string(img)
    if text: 
        print(text)   
        return text
    return None