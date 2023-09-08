from test.utils import equal_images_within_margin

from benevolent.replacer import replace_coded_text_boxes

TOLERABLE_ERROR_MARGIN = 2.0  # Eyeballed it, feel free to change if necessary.


def test_textbox_replacing(image_hello_world_encoded, image_hello_world_decoded, simple_sub_cipher):
    """Test correct replacing of text boxes."""
    text_boxes = [{'text': 'gpech', 'xy': [(58, 22), (288, 186)]}, {'text': 'uhbew', 'xy': [(308, 214), (540, 322)]}]
    result_image = replace_coded_text_boxes(image_hello_world_encoded, text_boxes, simple_sub_cipher)

    assert equal_images_within_margin(image_hello_world_decoded, result_image, TOLERABLE_ERROR_MARGIN)
