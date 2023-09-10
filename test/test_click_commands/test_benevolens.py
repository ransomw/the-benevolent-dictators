from pathlib import Path
from test.utils import equal_images_within_margin

from click.testing import CliRunner
from PIL import Image

from benevolent.cli import benevolens, benevolens_segments

TOLERABLE_ERROR_MARGIN = 5.0  # Eyeballed it, feel free to change if necessary.


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
    assert result.exit_code == 0

    with Image.open(path_result) as result:
        assert equal_images_within_margin(image_hello_world_decoded, result, TOLERABLE_ERROR_MARGIN)


def test_benevolens_segments(tmp_path, image_messy_hello_world_half_decoded):
    """Test image reading, decoding and writing."""
    path_original_image = Path("test") / "images" / "hello_world_encoded_2.jpg"
    path_result = Path(tmp_path) / "result.bmp"

    result = CliRunner().invoke(benevolens_segments,
                                [str(path_original_image.resolve()),
                                 "--cipher-seed", "abcd",
                                 "--format", "bmp",
                                 "141", "91", "280", "145",
                                 str(path_result.resolve())
                                 ])

    assert result.exit_code == 0

    with Image.open(path_result) as result:
        assert equal_images_within_margin(image_messy_hello_world_half_decoded, result, TOLERABLE_ERROR_MARGIN)
