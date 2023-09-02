import numpy as np
from PIL import Image


def create_xor_code(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """Returns an image obtained from the bitwise xor of the two input images.

    The resulting XOR image can be used with one of the two original images
    to obtain the other image:

    image1 ^ image2    = xor_image
    image1 ^ xor_image = image2
    image2 ^ xor_image = image1
    """
    if image1.size != image2.size:
        raise ValueError("input images must have the same size for XOR operation")

    image1_array, image2_array = np.asarray(image1), np.asarray(image2)

    return Image.fromarray(image1_array ^ image2_array)
