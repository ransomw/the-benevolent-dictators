import numpy as np
from PIL import Image


def equal_images(image_1: Image.Image, image_2: Image.Image) -> bool:
    """Returns True when both input images are equal."""
    return (np.asarray(image_1) == np.asarray(image_2)).all()
