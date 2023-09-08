from pathlib import Path
from test.conftest import IN_GITHUB_ACTIONS
from test.utils import equal_images_within_margin

import pytest
from click.testing import CliRunner
from PIL import Image

from benevolent.cli import box_write

TOLERABLE_ERROR_MARGIN = 5.0  # Eyeballed it, feel free to change if necessary.


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
