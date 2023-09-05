from test.utils import equal_images

from PIL import Image

from benevolent.writer import Writer


def test_write_hello_world(tmp_path, image1, image1_hello_world):
    """Write hello world to an image"""
    path = tmp_path / "writer_result.bmp"
    writer1 = Writer(image1, 36)
    writer1.write_text_box("hello world", (0, 0))
    image1.save(path)

    with Image.open(path) as result:
        assert equal_images(image1_hello_world, result)
