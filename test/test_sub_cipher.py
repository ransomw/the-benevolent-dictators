from benevolent.sub_cipher import (
    encode_simple_sub_cipher,
    decode_simple_sub_cipher,
)


def test_encode_decode_hello_world(simple_sub_cipher):
    """Encode and decode a string"""
    text = "Hello, world!"
    encoded_text = encode_simple_sub_cipher(simple_sub_cipher, text)
    decoded_text = decode_simple_sub_cipher(simple_sub_cipher, encoded_text)
    assert text != encoded_text, "dependent on this particular cipher"
    assert text == decoded_text
