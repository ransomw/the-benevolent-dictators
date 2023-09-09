from test.utils import equal_images_within_margin

import benevolent.sub_cipher as sc
from benevolent.translator import translate_chunks

TOLERABLE_ERROR_MARGIN = 5.0  # Eyeballed it, feel free to change if necessary.


def test_chunk_translation(image_messy_hello_world, image_messy_hello_world_decoded):
    """Test translating an image in chunks."""
    result = translate_chunks(image_messy_hello_world,
                              sc.generate_seeded_sub_cipher("abcd"),
                              [(141, 91, 280, 145), (817, 343, 984, 394)]
                              )

    assert equal_images_within_margin(image_messy_hello_world_decoded, result, TOLERABLE_ERROR_MARGIN)


def test_clean_translation(image_clean_hello_world, image_clean_hello_world_decoded):
    """Test translating a clean image in chunks.

    I just wanted to see our programm nailing a translation for once XD
    """
    result = translate_chunks(image_clean_hello_world,
                              sc.generate_seeded_sub_cipher("abcd"),
                              [(231, 166, 440, 251), (1108, 555, 1318, 638)]
                              )

    assert equal_images_within_margin(image_clean_hello_world_decoded, result, TOLERABLE_ERROR_MARGIN)
