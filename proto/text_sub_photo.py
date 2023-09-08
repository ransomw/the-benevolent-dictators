"""
these are various attempts to cleanup photos for input into tesseract
https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
so far, there's very little success
"""
import os
import sys

from writer import Writer

sys.path.insert(0, os.path.abspath('.'))
import string
from pathlib import Path

import numpy as np
from PIL import (
    Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
)
from pytesseract import Output as PytesseractOutput
from pytesseract import image_to_boxes, image_to_data, image_to_string
from skimage.filters import threshold_otsu

from benevolent.ocr import (
    img_to_mono__norm_and_otsu,
)
from benevolent.sub_cipher import (
    decode_simple_sub_cipher, load_simple_sub_cipher
)

img_path = Path(__file__).parent / "hello_world_encoded_02.jpg"
font_path = Path(__file__).parent.parent / "fonts" / "FreeMono.ttf"
cipher_path = Path(__file__).parent.parent / "test" / "ciphers" / "simple_sub_01.cipher"

font = ImageFont.truetype(str(font_path), 32)
cipher = load_simple_sub_cipher(cipher_path)
img = Image.open(img_path)

img_mono = img_to_mono__norm_and_otsu(img)

img_to_ocr = img_mono.resize(
    tuple(c//2 for c in img_mono.size),
    resample=Image.Resampling.LANCZOS
)

# img_to_ocr = img_mono

# img_to_ocr = img_mono.thumbnail(
#     tuple(c//2 for c in img_mono.size),
#     resample=Image.Resampling.LANCZOS
# )


# data_string = image_to_string(img_to_ocr)

data_dict = image_to_data(
    img_to_ocr,
    output_type=PytesseractOutput.DICT,
    config=f"-c tessedit_char_whitelist=\"{string.ascii_lowercase}\"",
)

def pytess_dict_to_text_and_boxes(data):
    text_and_boxes = []
    for (idx, text) in enumerate(data['text']):
        if not text:
            continue
        x0 = data['left'][idx]
        y0 = data['top'][idx]
        x1 = x0 + data['width'][idx]
        y1 = y0 + data['height'][idx]
        text_and_boxes.append({
            'text': text,
            'xy': [(x0, y0), (x1, y1)],
        })
    return text_and_boxes

# print(string)

text_and_boxes = pytess_dict_to_text_and_boxes(data_dict)

# ---- BAUTISTA -----
img_with_boxes = img_to_ocr.copy().convert("RGB")
wr = Writer(img_with_boxes, 32)
for tnb in text_and_boxes:
    wr.write_text_box(decode_simple_sub_cipher(cipher, tnb['text']), tnb["xy"][0])
img_with_boxes.save(Path("proto") / "debug_images" / "test.jpg")

# TEST 2
wr = Writer(img, 32*2)
for tnb in text_and_boxes:
    wr.draw_box([tuple(c * 2 for c in t)
                 for t in tnb["xy"]])
    wr.write_text_box(decode_simple_sub_cipher(cipher, tnb['text']), tuple(c * 2 for c in tnb["xy"][0]))

img.save(Path("proto") / "debug_images" / "test2.jpg")
# ----------- END OF BAUTISTA ------

img_with_boxes = img_to_ocr.copy()
draw_boxes = ImageDraw.Draw(img_with_boxes)
for tnb in text_and_boxes:
    xy = tnb['xy']
    print(xy)
    draw_boxes.rectangle(xy, outline=0)


img_with_text = img_to_ocr.copy()
draw_text = ImageDraw.Draw(img_with_text)
for tnb in text_and_boxes:
    text = decode_simple_sub_cipher(cipher, tnb['text'])
    bbox = font.getbbox(text)
    text_img = Image.new("RGBA", (bbox[2], bbox[3]), "black")
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((0,0), text, font=font, fill=(255,255,255))
    xy = tnb['xy']
    p0, p1 = xy
    x0, y0 = p0
    x1, y1 = p1
    text_img_resized = text_img.resize((x1-x0, y1-y0))
    img_with_text.paste(text_img_resized, p0)
img_with_text.save("test2.jpg")


#breakpoint()
