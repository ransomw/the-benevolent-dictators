import pytesseract
from PIL import Image

def get_image_text(image: Image.Image) -> str:
    """Returns text from an image"""
    return pytesseract.image_to_string(image)

