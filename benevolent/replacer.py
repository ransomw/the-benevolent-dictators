from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import benevolent.sub_cipher as sc
from benevolent.writer import Writer

PADDING = 10


def replace_coded_text_boxes(image: Image.Image,
                             coded_text_and_boxes,
                             cipher: sc.SimpleSubCipher
                             ) -> Image.Image:
    """Replaces coded text from an image with decoded text."""
    output_image = image.copy()
    for text_box in coded_text_and_boxes:
        wr = Writer(output_image, get_text_size(image, text_box))
        wr.draw_box(text_box["xy"])
        wr.write_text(sc.decode_simple_sub_cipher(cipher, text_box["text"]), text_box["xy"][0])
    return output_image


def get_text_size(image, text_box):
    """Return the ideal text size for this text box."""
    draw = ImageDraw.Draw(image)
    box_length = text_box["xy"][1][0] - text_box["xy"][0][0]

    jump_size = 64
    font_size = 64
    font = load_font(font_size)
    while True:
        if draw.textlength(text_box["text"], font=font) < (box_length - PADDING):
            font_size += jump_size
        else:
            jump_size = jump_size // 2
            font_size -= jump_size
        font = load_font(font_size)
        if jump_size < 1:
            return font_size


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """Load and return a ttp font."""
    font_path = str((Path("fonts") / "FreeMono.ttf").absolute())
    return ImageFont.truetype(font_path, size)
