import string

import numpy as np
import pytesseract
from PIL import Image, ImageFilter, ImageOps
from pytesseract import Output as PytesseractOutput
from pytesseract import image_to_data
from skimage.filters import threshold_otsu

import benevolent.sub_cipher as sc
from benevolent.conf import get_config
from benevolent.replacer import replace_coded_text_boxes


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


def translate_image(image: Image.Image,
                    cipher: sc.SimpleSubCipher
                    ) -> Image.Image:
    """Reads an image with pytesseract and outputs a translated image."""
    text_boxes = _get_textboxes(image)
    return replace_coded_text_boxes(image, text_boxes, cipher)


def _get_textboxes(image: Image.Image):
    img_mono = img_to_mono(image.copy())
    data_dict = image_to_data(
        img_mono,
        output_type=PytesseractOutput.DICT,
        config=f"-c tessedit_char_whitelist=\"{string.ascii_letters}\"",
    )
    text_and_boxes = []
    for (idx, text) in enumerate(data_dict['text']):
        if not text:
            continue
        x0 = data_dict['left'][idx]
        y0 = data_dict['top'][idx]
        x1 = x0 + data_dict['width'][idx]
        y1 = y0 + data_dict['height'][idx]
        text_and_boxes.append({
            'text': text,
            'xy': [(x0, y0), (x1, y1)],
        })
    return text_and_boxes


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
