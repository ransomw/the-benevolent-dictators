from pathlib import Path
from test.utils import equal_images

from click.testing import CliRunner
from PIL import Image

from benevolent.cli import xor_code


def test_xor_image_is_created(tmp_path, xord_image):
    """Test that the correct XOR image is created when running the xor-code command."""
    path = tmp_path / "xor_result.jpg"
    path_acolchado = Path("test") / "images" / "acolchado.jpg"
    path_sheet = Path("test") / "images" / "sheet.jpg"

    result = CliRunner().invoke(xor_code, [str(path_acolchado.resolve()),
                                           str(path_sheet.resolve()),
                                           str(path.resolve())])
    assert result.exit_code == 0

    with Image.open(path) as result:
        assert equal_images(xord_image, result)


def test_xor_decode(tmp_path):
    """Test decoding image with .bmps"""
    xor_result_path = tmp_path / "xor_result.bmp"
    xor_decode_path = tmp_path / "xor_decode.bmp"
    path_acolchado = Path("test") / "images" / "acolchado.bmp"
    path_sheet = Path("test") / "images" / "sheet.bmp"

    result = CliRunner().invoke(xor_code, [str(path_acolchado.resolve()),
                                           str(path_sheet.resolve()),
                                           str(xor_result_path.resolve())])
    assert result.exit_code == 0
    result = CliRunner().invoke(xor_code, [str(path_acolchado.resolve()),
                                           str(xor_result_path.resolve()),
                                           str(xor_decode_path.resolve())])
    assert result.exit_code == 0

    with Image.open(path_sheet) as sheet_image, Image.open(
            xor_decode_path) as decoded_image:
        assert equal_images(sheet_image, decoded_image)
