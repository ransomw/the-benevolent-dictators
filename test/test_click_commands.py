from pathlib import Path
from test.conftest import IN_GITHUB_ACTIONS
from test.utils import equal_images, equal_images_within_margin

import pytest
from click.testing import CliRunner
from PIL import Image

import benevolent.sub_cipher as sc
from benevolent.cli import (
    benevolens, box_write, decode_with_cipher, encode_with_cipher,
    generate_cipher, xor_code
)

TOLERABLE_ERROR_MARGIN = 5.0  # Eyeballed it, feel free to change if necessary.


def test_xor_image_is_created(tmp_path, xord_image):
    """Test that the correct XOR image is created when running the xor-code command."""
    path = tmp_path / "xor_result.jpg"
    path_acolchado = Path("test") / "images" / "acolchado.jpg"
    path_sheet = Path("test") / "images" / "sheet.jpg"
    CliRunner().invoke(xor_code, [str(path_acolchado.resolve()),
                                  str(path_sheet.resolve()),
                                  str(path.resolve())])

    with Image.open(path) as result:
        assert equal_images(xord_image, result)


def test_xor_decode(tmp_path):
    """Test decoding image with .bmps"""
    xor_result_path = tmp_path / "xor_result.bmp"
    xor_decode_path = tmp_path / "xor_decode.bmp"
    path_acolchado = Path("test") / "images" / "acolchado.bmp"
    path_sheet = Path("test") / "images" / "sheet.bmp"
    CliRunner().invoke(xor_code, [str(path_acolchado.resolve()),
                                  str(path_sheet.resolve()),
                                  str(xor_result_path.resolve())])

    CliRunner().invoke(xor_code, [str(path_acolchado.resolve()),
                                  str(xor_result_path.resolve()),
                                  str(xor_decode_path.resolve())])

    with Image.open(path_sheet) as sheet_image, Image.open(
            xor_decode_path) as decoded_image:
        assert equal_images(sheet_image, decoded_image)


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Images are saved differently in GH actions env.")
def test_text_is_written(tmp_path, image1_hello_world_bmp):
    """Test writting to a bmp image."""
    original_image_path = Path("test") / "images" / "acolchado.bmp"
    write_result_path = tmp_path / "write_result.bmp"

    CliRunner().invoke(box_write, [str(original_image_path.resolve()),
                                   "hello world",
                                   "--size", 36,
                                   "-x", 0,
                                   "-y", 0,
                                   str(write_result_path.resolve())])

    with Image.open(write_result_path) as result:
        assert equal_images_within_margin(image1_hello_world_bmp, result, TOLERABLE_ERROR_MARGIN)


def test_encoding():
    """Test encoding text from the cli."""
    cipher_path = Path("test") / "ciphers" / "simple_sub_01.cipher"
    runner = CliRunner()
    result = runner.invoke(encode_with_cipher,
                           ["hello world",
                            "--cipher-path", str(cipher_path.resolve())])

    assert result.exit_code == 0
    assert result.output == "gpcch uhbcw\n"


def test_decoding():
    """Test decoding text from the cli."""
    cipher_path = Path("test") / "ciphers" / "simple_sub_01.cipher"
    runner = CliRunner()
    result = runner.invoke(decode_with_cipher,
                           ["gpcch uhbcw",
                            "--cipher-path", str(cipher_path.resolve())])

    assert result.exit_code == 0
    assert result.output == "hello world\n"


def test_seeded_encoding():
    """Test encoding with a given seed."""
    runner = CliRunner()
    result = runner.invoke(encode_with_cipher,
                           ["hello world",
                            "--cipher-seed", 1234])

    assert result.exit_code == 0
    assert result.output == "gqllc icnlv\n"


def test_seeded_decoding():
    """Test decoding with a given seed."""
    runner = CliRunner()
    result = runner.invoke(decode_with_cipher,
                           ["gqllc icnlv",
                            "--cipher-seed", 1234])

    assert result.exit_code == 0
    assert result.output == "hello world\n"


def test_seeded_cipher_generating(tmp_path):
    """Test generating a cipher with a seed."""
    path_expected_cipher = Path("test") / "ciphers" / "seeded_1234.cipher"
    path_generated_cipher = Path(tmp_path) / "generated_1234.cipher"
    runner = CliRunner()
    result = runner.invoke(generate_cipher,
                           [str(path_generated_cipher.resolve()),
                            "--cipher-seed", 1234])

    assert result.exit_code == 0

    expected_cipher = sc.load_cipher(path_expected_cipher)
    generated_cipher = sc.load_cipher(path_generated_cipher)
    assert expected_cipher == generated_cipher


def test_benevolens(tmp_path, image_hello_world_decoded):
    """Test image reading, decoding and writing."""
    path_original_image = Path("test") / "images" / "handwriting_hello_world_encoded.jpg"
    path_cipher = Path("test") / "ciphers" / "simple_sub_01.cipher"
    path_result = Path(tmp_path) / "result.bmp"

    result = CliRunner().invoke(benevolens,
                                [str(path_original_image.resolve()),
                                 "--cipher-path", str(path_cipher.resolve()),
                                 "--format", "bmp",
                                 str(path_result.resolve())
                                 ])

    with Image.open(path_result) as result:
        assert equal_images_within_margin(image_hello_world_decoded, result, TOLERABLE_ERROR_MARGIN)
