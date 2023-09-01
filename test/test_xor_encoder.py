import numpy as np
from PIL import Image

from xor_enconder import create_xor_code

image1_path = "test/images/acolchado.jpg"
image2_path = "test/images/sheet.jpg"


def test_same_xor_both_ways():
    """Tests that the order of the images doesn't change the resulting xor image."""
    image1, image2 = Image.open(image1_path), Image.open(image2_path)

    assert equal_images(create_xor_code(image1, image2), create_xor_code(image2, image1))

    image1.close()
    image2.close()


def test_original_image_is_obtained():
    """Tests that the original images can be reconstructed with the obtained xor image."""
    image1, image2 = Image.open(image1_path), Image.open(image2_path)
    xor_image = create_xor_code(image1, image2)

    assert equal_images(image1, create_xor_code(image2, xor_image)) and \
           equal_images(image2, create_xor_code(image1, xor_image))

    image1.close()
    image2.close()


def equal_images(image1: Image.Image, image2: Image.Image) -> bool:
    """Returns True when both input images are equal."""
    return (np.asarray(image1) == np.asarray(image2)).all()
