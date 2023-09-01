import subprocess
from pathlib import Path
from test.utils import equal_images

import pytest
from PIL import Image


@pytest.fixture
def xord_image():
    """Create xord_image and automatically close after test."""
    path = Path("test") / "images" / "xord_image.jpg"
    with Image.open(path) as image:
        yield image


def test_xor_image_is_created(tmp_path, xord_image):
    """Test that the correct XOR image is created when running the xor-code command."""
    path = Path(tmp_path) / "xor_result.jpg"
    subprocess.run(["python", "-m", "benevolent", "xor-code", "--path1", "test/images/acolchado.jpg",
                    "--path2", "test/images/sheet.jpg", "--path-out", str(path.absolute())])

    with Image.open(path) as result:
        assert equal_images(xord_image, result)
