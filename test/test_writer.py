from test.utils import equal_images

import shutil
from PIL import Image

from benevolent.writer import Writer


def test_write_hello_world(tmp_path, image1_bmp, image1_hello_world_bmp):
    """Write hello world to an image"""
    path = tmp_path / "writer_result.bmp"
    writer1 = Writer(image1_bmp, 36)
    writer1.write_text_box("hello world", (0, 0))
    image1_bmp.save(path)

    shutil.copyfile(path, "out.bmp")

    # with Image.open(path) as result:
    #     assert equal_images(image1_hello_world_bmp, result)
