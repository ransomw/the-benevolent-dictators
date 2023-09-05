from benevolent.ocr import get_image_text


def test_hello_world_image(image_hello_world):
    """Read text from a black and white image"""
    text = get_image_text(image_hello_world)
    assert text.strip() == 'hello world'
