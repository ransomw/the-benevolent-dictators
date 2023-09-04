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


def test_xor_decode(tmp_path):
    xor_result_path = tmp_path / "xor_result.bmp"
    xor_decode_path = tmp_path / "xor_decode.bmp"
    CliRunner().invoke(xor_code, ["test/images/acolchado.bmp",
                                  "test/images/sheet.bmp",
                                  str(xor_result_path.resolve())])

    CliRunner().invoke(xor_code, ["test/images/acolchado.bmp",
                                  str(xor_result_path.resolve()),
                                  str(xor_decode_path.resolve())])

    with Image.open("test/images/sheet.bmp") as sheet_image, Image.open(xor_decode_path) as decoded_image:
        assert equal_images(sheet_image, decoded_image)

