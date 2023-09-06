import os
from pathlib import Path

import pytest
from PIL import Image

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
def xord_image():
    """Create xord_image and automatically close after test."""
    path = Path("test") / "images" / "xord_image.jpg"
    with Image.open(path) as image:
        yield image
