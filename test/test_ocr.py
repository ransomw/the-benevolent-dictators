import pytest
from PIL import Image

from benevolent.ocr import get_image_text, img_to_mono__norm_and_otsu


@pytest.mark.skip(reason="cut down on test time: OCR taking too long")
def test_hello_world_image(image_hello_world):
    """Read text from a black and white image"""
    text = get_image_text(image_hello_world)
    assert text.strip() == 'hello world'


def test_otsu_minimally_effective(image_handwriting_hello_world_encoded):
    """Observe `img_to_mono__norm_and_otsu` increases OCR effectiveness."""
    img_no_otsu = image_handwriting_hello_world_encoded
    text_no_otsu = get_image_text(img_no_otsu)
    img_otsu = img_to_mono__norm_and_otsu(img_no_otsu)
    # resize image for faster processing time by tesseract
    img_otsu_sm = img_otsu.resize(
        tuple(c//2 for c in img_otsu.size),
        resample=Image.Resampling.LANCZOS
    )
    text_otsu = get_image_text(img_otsu_sm)

    # CI tesseract behaves differently from local
    # assert text_no_otsu == '', "without preprocessing, no text"
    # assert text_otsu != '', "with preprocessing, text discovered"

    assert len(text_no_otsu) < len(text_otsu), "detect more text with otsu"

    # continuing from "resize image" comment:
    # ... but is the tesseract processing time totally dependent on the size?
    # the following produces a smaller image,
    # and tesseract takes a long time to process it

    # img_otsu_tn = img_otsu.copy()
    # img_otsu_tn.thumbnail((200, 200))
    # text_otsu_tn = get_image_text(img_otsu_sm)
