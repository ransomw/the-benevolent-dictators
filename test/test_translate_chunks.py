import benevolent.sub_cipher as sc
from benevolent.translate_chunks import translate_chunks


def test_chunk_translation(image_messy_hello_world):
    """Test translating an image in chunks."""
    translate_chunks(image_messy_hello_world,
                     sc.generate_seeded_sub_cipher("abcd"),
                     [(141, 91, 280, 145), (817, 343, 984, 394)]
                     ).save("prueba2.jpg")

    assert "h" == sc.encode_simple_sub_cipher(sc.generate_seeded_sub_cipher("abcd"), "hello world")


def test_clean_translation(image_clean_hello_world):
    """Test translating a clean image in chunks.

    I just wanted to see our programm nailing a translation for once XD
    """
    translate_chunks(image_clean_hello_world,
                     sc.generate_seeded_sub_cipher("abcd"),
                     [(231, 166, 440, 251), (1108, 555, 1318, 638)]
                     ).save("prueba3.jpg")

    assert "h" == sc.encode_simple_sub_cipher(sc.generate_seeded_sub_cipher("abcd"), "hello world")
