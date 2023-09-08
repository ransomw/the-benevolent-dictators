import numpy as np
from PIL import Image


def equal_images(image_1: Image.Image, image_2: Image.Image) -> bool:
    """Returns True when both input images are equal."""
    return (np.asarray(image_1) == np.asarray(image_2)).all()


def equal_images_within_margin(image_1: Image.Image, image_2: Image.Image, error_margin: float) -> bool:
    """Return True when the percentage of differences within each image is bellow the error_margin."""
    percentage_of_dissimilarity = percentage_false((np.asarray(image_1) == np.asarray(image_2)))
    return percentage_of_dissimilarity < error_margin


def percentage_false(array: np.ndarray) -> float:
    """Return the percentage of Falses in the array."""
    trues = np.sum(array == True)    # noqa: E712
    falses = np.sum(array == False)  # noqa: E712
    total = trues + falses
    return (falses / total) * 100
