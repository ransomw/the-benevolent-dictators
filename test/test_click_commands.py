from test.utils import equal_images

from click.testing import CliRunner
from PIL import Image

from benevolent.cli import xor_code


def test_xor_image_is_created(tmp_path, xord_image):
    """Test that the correct XOR image is created when running the xor-code command."""
    path = tmp_path / "xor_result.jpg"
    CliRunner().invoke(xor_code, ["test/images/acolchado.jpg",
                                  "test/images/sheet.jpg",
                                  str(path.resolve())])

    with Image.open(path) as result:
        assert equal_images(xord_image, result)
