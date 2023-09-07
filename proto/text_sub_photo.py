"""
these are various attempts to cleanup photos for input into tesseract
https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
so far, there's very little success
"""
from pathlib import Path
from pytesseract import (
    image_to_string,
    image_to_boxes,
    image_to_data,
)
from PIL import (
    Image,
    ImageOps,
    ImageEnhance,
    ImageFilter,
)


img_path = Path(__file__).parent / "hello_world_encoded_01.jpg"
img_path = Path(__file__).parent / "hello_world_encoded_02.jpg"



img = Image.open(img_path)


threshold = 120


# img_grayscale = img.convert('L')
img_grayscale = ImageOps.grayscale(img)

img_edges = img_grayscale.filter(ImageFilter.FIND_EDGES)
img_edges = img_grayscale.filter(ImageFilter.EDGE_ENHANCE)
img_sharpened = img_grayscale.filter(ImageFilter.SHARPEN)



img_autocontrast = ImageOps.autocontrast(img_grayscale, cutoff=10)


img_contrast = img_grayscale.copy()
contast_enhancer = ImageEnhance.Contrast(img_contrast)
contast_enhancer.enhance(0.2)


img_sharp = img_contrast.copy()
sharp_enhancer = ImageEnhance.Sharpness(img_sharp)
sharp_enhancer.enhance(2.0)

img_thres = img_sharp.point( lambda p: 255 if p > threshold else 0 )

img_thres_1 = img_edges.point( lambda p: 255 if p > threshold else 0 )

img_mono = img_thres.convert('1')


string = image_to_string(img)
boxes = image_to_boxes(img)
data = image_to_data(img)

print(string)
print(boxes)
print(data)

breakpoint()

