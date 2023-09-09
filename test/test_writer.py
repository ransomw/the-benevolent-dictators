from test.utils import equal_images_within_margin

from benevolent.writer import Writer

TOLERABLE_ERROR_MARGIN = 5.0


def test_write_hello_world(image1_bmp, image1_hello_world_bmp):
    """Write hello world to an image"""
    writer1 = Writer(image1_bmp, 36)
    writer1.write_text_box("hello world", (0, 0))

    assert equal_images_within_margin(image1_hello_world_bmp, image1_bmp, TOLERABLE_ERROR_MARGIN)
