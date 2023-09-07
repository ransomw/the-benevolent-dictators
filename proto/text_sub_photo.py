"""
these are various attempts to cleanup photos for input into tesseract
https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
so far, there's very little success
"""
import sys, os
sys.path.insert(0, os.path.abspath('.'))
import string
import numpy as np
from pathlib import Path
from pytesseract import (
    image_to_string,
    image_to_boxes,
    image_to_data,
    Output as PytesseractOutput,
)
from PIL import (
    Image,
    ImageOps,
    ImageEnhance,
    ImageFilter,
    ImageDraw,
    ImageFont,
)
from skimage.filters import threshold_otsu
from benevolent.sub_cipher import (
    load_simple_sub_cipher,
    decode_simple_sub_cipher,
)

img_path = Path(__file__).parent / "hello_world_encoded_02.jpg"
font_path = Path(__file__).parent.parent / "fonts" / "FreeMono.ttf"
cipher_path = Path(__file__).parent.parent / "test" / "ciphers" / "simple_sub_01.cipher"

font = ImageFont.truetype(str(font_path), 32)
cipher = load_simple_sub_cipher(cipher_path)
img = Image.open(img_path)


img_gray = ImageOps.grayscale(img)

img_blur1 = img_gray.filter(ImageFilter.BoxBlur(3))
img_blur2 = img_gray.filter(ImageFilter.BoxBlur(50))

arr_blur1 = np.asarray(img_blur1)
arr_blur2 = np.asarray(img_blur2)
arr_divided = np.ma.divide(arr_blur1, arr_blur2).data
arr_normed = np.uint8(255*arr_divided/arr_divided.max())

otsu_thres = threshold_otsu(arr_normed)

print(f"otsu threshold {otsu_thres}")

img_normed = Image.fromarray(arr_normed)

img_thres = img_normed.point( lambda p: 255 if p > otsu_thres else 0 )

img_mono = img_thres.convert('1')

img_to_ocr = img_mono.resize(
    tuple(c//2 for c in img_mono.size),
    resample=Image.Resampling.LANCZOS
)

# img_to_ocr = img_mono

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

img_with_boxes = img_to_ocr.copy()
draw_boxes = ImageDraw.Draw(img_with_boxes)
for tnb in text_and_boxes:
    xy = tnb['xy']
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


breakpoint()
