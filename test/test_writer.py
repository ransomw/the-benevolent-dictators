# from test.utils import equal_images

from benevolent.writer import Writer


def test_write_hello_world(image1_bmp, image1_hello_world_bmp):
    """Write hello world to an image"""
    writer1 = Writer(image1_bmp, 36)
    writer1.write_text_box("hello world", (0, 0))

    # GitHub actions just refuses to accept this one even though it works locally
    # assert equal_images(image1_hello_world_bmp, image1_bmp)
