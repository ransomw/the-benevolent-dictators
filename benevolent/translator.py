from PIL import Image

import benevolent.sub_cipher as sc
from benevolent.ocr import get_tesseract_data
from benevolent.replacer import replace_coded_text_boxes


def translate_chunks(image: Image.Image,
                     cipher: sc.SimpleSubCipher,
                     chunks: list[tuple[int, int, int, int]]
                     ) -> Image.Image:
    """Translate images in chunks, to hopefully increase tesseract accuracy."""
    image_out = image.copy()
    for chunk in chunks:
        translated_chunk = translate_image(image.crop(chunk), cipher)
        image_out.paste(translated_chunk, chunk)
    return image_out


def translate_image(image: Image.Image,
                    cipher: sc.SimpleSubCipher
                    ) -> Image.Image:
    """Reads an image with pytesseract and outputs a translated image."""
    text_boxes = _get_textboxes(image)
    return replace_coded_text_boxes(image, text_boxes, cipher)


def _get_textboxes(image: Image.Image):
    data_dict = get_tesseract_data(image)
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
