from PIL import Image

import benevolent.sub_cipher as sc
from benevolent.writer import Writer


def replace_coded_text_boxes(image: Image.Image, coded_text_and_boxes, cipher) -> Image.Image:
    """Replaces coded text from an image with decoded text."""
    output_image = image.copy()
    for text_box in coded_text_and_boxes:
        wr = Writer(output_image, get_text_size(image, text_box))
        wr.draw_box(text_box["xy"])
        wr.write_text(sc.decode_simple_sub_cipher(cipher, text_box["text"]), text_box["xy"][0])
    return output_image


def get_text_size(image, text_box):
    """TODO: return the ideal text size for this text box."""
    return 64
