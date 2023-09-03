from test.utils import equal_images

from benevolent.xor_enconder import create_xor_code


def test_same_xor_both_ways(image1, image2):
    """Tests that the order of the images doesn't change the resulting xor image."""
    assert equal_images(create_xor_code(image1, image2), create_xor_code(image2, image1))


def test_original_image_is_obtained(image1, image2):
    """Tests that the original images can be reconstructed with the obtained xor image."""
    xor_image = create_xor_code(image1, image2)

    assert equal_images(image1, create_xor_code(image2, xor_image)) and \
           equal_images(image2, create_xor_code(image1, xor_image))
