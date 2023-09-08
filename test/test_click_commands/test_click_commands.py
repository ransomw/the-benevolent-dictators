from pathlib import Path
from test.utils import equal_images_within_margin

from click.testing import CliRunner
from PIL import Image

from benevolent.cli import benevolens

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

    with Image.open(path_result) as result:
        assert equal_images_within_margin(image_hello_world_decoded, result, TOLERABLE_ERROR_MARGIN)
