from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from xor_enconder import create_xor_code


@pytest.fixture
def image1():
    """Create image1 and automatically close after test."""
    path = Path("test") / "images" / "acolchado.jpg"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image2():
    """Create image2 and automatically close after test."""
    path = Path("test") / "images" / "sheet.jpg"
    with Image.open(path) as image:
        yield image


def test_same_xor_both_ways(image1, image2):
    """Tests that the order of the images doesn't change the resulting xor image."""
    assert equal_images(create_xor_code(image1, image2), create_xor_code(image2, image1))


def test_original_image_is_obtained(image1, image2):
    """Tests that the original images can be reconstructed with the obtained xor image."""
    xor_image = create_xor_code(image1, image2)

    assert equal_images(image1, create_xor_code(image2, xor_image)) and \
           equal_images(image2, create_xor_code(image1, xor_image))


def equal_images(image_1: Image.Image, image_2: Image.Image) -> bool:
    """Returns True when both input images are equal."""
    return (np.asarray(image_1) == np.asarray(image_2)).all()
