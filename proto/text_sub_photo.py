"""
these are various attempts to cleanup photos for input into tesseract
https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
so far, there's very little success
"""
import numpy as np
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
from skimage.filters import threshold_otsu

img_path = Path(__file__).parent / "hello_world_encoded_01.jpg"
img_path = Path(__file__).parent / "hello_world_encoded_02.jpg"

img = Image.open(img_path)


threshold = 100

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

breakpoint()

string = image_to_string(img_mono)
# boxes = image_to_boxes(img_mono)
# data = image_to_data(img_mono)

print(string)
# print(boxes)
# print(data)

breakpoint()

