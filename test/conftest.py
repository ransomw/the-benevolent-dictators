import os
from pathlib import Path

import pytest
from PIL import Image

from benevolent import sub_cipher

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.fixture
def image1():
    """Create image1 and automatically close after test."""
    path = Path("test") / "images" / "acolchado.jpg"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image1_bmp():
    """Create image1 and automatically close after test."""
    path = Path("test") / "images" / "acolchado.bmp"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image1_hello_world_bmp():
    """Create image1 and automatically close after test."""
    path = Path("test") / "images" / "acolchado_hello_world.bmp"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image2():
    """Create image2 and automatically close after test."""
    path = Path("test") / "images" / "sheet.jpg"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image3():
    """Create image3, that has a different size to 1 and 2. Automatically close it after test."""
    path = Path("test") / "images" / "dog.jpg"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image_hello_world():
    """Create image3, that has a different size to 1 and 2. Automatically close it after test."""
    path = Path("test") / "images" / "hello_world.bmp"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image_handwriting_hello_world_encoded():
    """A handwritten message, "hello world," encoded using `sub_cipher`"""
    path = Path("test") / "images" / "handwriting_hello_world_encoded.jpg"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def xord_image():
    """Create xord_image and automatically close after test."""
    path = Path("test") / "images" / "xord_image.jpg"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image_hello_world_encoded():
    """Create the handwriting hello world encoded image."""
    path = Path("test") / "images" / "handwriting_hello_world_encoded.jpg"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def image_hello_world_decoded():
    """Create the handwriting hello world decoded image."""
    path = Path("test") / "images" / "handwriting_hello_world_decoded.bmp"
    with Image.open(path) as image:
        yield image


@pytest.fixture
def simple_sub_cipher():
    """Load the .cipher file into an object"""
    path = Path("test") / "ciphers" / "simple_sub_01.cipher"
    return sub_cipher.load_cipher(path)
