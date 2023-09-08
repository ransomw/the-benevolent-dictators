import numpy as np
import pytesseract
from PIL import Image, ImageFilter, ImageOps
from skimage.filters import threshold_otsu

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


def img_to_mono(
        img,
        font_blur=3,
        background_blur=50,
):
    """
    Prepare an image for input to tesseract.

    https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
    """
    img_gray = ImageOps.grayscale(img)

    img_blur1 = img_gray.filter(ImageFilter.BoxBlur(font_blur))
    img_blur2 = img_gray.filter(ImageFilter.BoxBlur(background_blur))

    arr_blur1 = np.asarray(img_blur1)
    arr_blur2 = np.asarray(img_blur2)
    arr_divided = np.ma.divide(arr_blur1, arr_blur2).data
    arr_normed = np.uint8(255*arr_divided/arr_divided.max())

    otsu_thres = threshold_otsu(arr_normed)

    img_normed = Image.fromarray(arr_normed)

    img_thres = img_normed.point(lambda p: 255 if p > otsu_thres else 0)

    img_mono = img_thres.convert('1')
    return img_mono


load_config()
