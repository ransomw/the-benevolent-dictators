from pathlib import Path

from click.testing import CliRunner

import benevolent.sub_cipher as sc
from benevolent.cli import (
    decode_with_cipher, encode_with_cipher, generate_cipher
)


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


def test_seeded_cipher_generating(tmp_path: Path):
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
