from typing import Any

import numpy as np
from PIL import Image


def equal_images(image_1: Image.Image, image_2: Image.Image) -> bool:
    """Returns True when both input images are equal."""
    return (np.asarray(image_1) == np.asarray(image_2)).all()


def equal_images_within_margin(image_1: Image.Image, image_2: Image.Image, error_margin: float) -> bool:
    """Return True when the percentage of differences within each image is bellow the error_margin."""
    percentage_of_dissimilarity = percentage((np.asarray(image_1) == np.asarray(image_2)), False)
    return percentage_of_dissimilarity < error_margin


def percentage(array: np.ndarray, value: Any) -> float:
    """Return the percentage of the given value in the array."""
    return np.sum(array == value)/array.shape[0]*100
