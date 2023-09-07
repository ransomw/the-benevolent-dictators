"""
* read text from an image with tesseract
* decode text using simple substitution cipher
* write text back into image a-la GG Lens

reading the text is feasible by using an image created using,
for example, gimp or MS Paint or paint(1), such that the image
can directly be fed into pytesseract.

there's a function for reshaping the pytesseract output that may be useful.

the trick to writing the text back into the image
is creating new images, resizing them to the boxes detected by tesseract,
and pasting them onto the original image.
"""
import sys, os
sys.path.insert(0, os.path.abspath('.'))
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
from benevolent.sub_cipher import (
    load_simple_sub_cipher,
    decode_simple_sub_cipher,
)

img_path = Path(__file__).parent / "hello_world_encoded_03.jpg"
font_path = Path(__file__).parent.parent / "fonts" / "FreeMono.ttf"
cipher_path = Path(__file__).parent.parent / "test" / "ciphers" / "simple_sub_01.cipher"

font = ImageFont.truetype(str(font_path), 32)
cipher = load_simple_sub_cipher(cipher_path)
img = Image.open(img_path)


# string = image_to_string(img)
# boxes = image_to_boxes(img)
data_dict = image_to_data(img, output_type=PytesseractOutput.DICT)

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


text_and_boxes = pytess_dict_to_text_and_boxes(data_dict)

img_with_boxes = img.copy()
draw_boxes = ImageDraw.Draw(img_with_boxes)
for tnb in text_and_boxes:
    xy = tnb['xy']
    draw_boxes.rectangle(xy, outline=0)


img_with_text = img.copy()
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

img_with_text.show()

breakpoint()

