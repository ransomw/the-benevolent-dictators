from pathlib import Path
from test.utils import equal_images_within_margin

from click.testing import CliRunner
from PIL import Image

import benevolent.sub_cipher as sc
from benevolent.cli import (
    benevolens, decode_with_cipher, encode_with_cipher, generate_cipher
)

TOLERABLE_ERROR_MARGIN = 5.0  # Eyeballed it, feel free to change if necessary.


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
