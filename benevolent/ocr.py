import pytesseract
from PIL import Image

from benevolent.conf import get_config


def load_config():
    """Set the tesseract command's path"""
    cfg = get_config()
    if cfg is None:
        return
    if 'tesseract' not in cfg:
        return
    if 'path' not in cfg['tesseract']:
        return
    pytesseract.pytesseract.tesseract_cmd = cfg['tesseract']['path']


def get_image_text(image: Image.Image) -> str:
    """Returns text from an image"""
    return pytesseract.image_to_string(image)


load_config()
