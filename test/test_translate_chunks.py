import benevolent.sub_cipher as sc
from benevolent.translate_chunks import translate_chunks


def test_chunk_translation(image_messy_hello_world):
    """Test translating an image in chunks."""
    translate_chunks(image_messy_hello_world,
                     sc.generate_seeded_sub_cipher("abcd"),
                     [(141, 91, 280, 145), (817, 343, 984, 394)]
                     ).save("prueba2.jpg")

    assert "h" == sc.encode_simple_sub_cipher(sc.generate_seeded_sub_cipher("abcd"), "hello world")
