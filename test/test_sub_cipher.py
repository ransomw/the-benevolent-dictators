from benevolent.sub_cipher import decode_text, encode_text


def test_encode_decode_hello_world(simple_sub_cipher):
    """Encode and decode a string"""
    text = "Hello, World!"
    encoded_text = encode_text(simple_sub_cipher, text)
    decoded_text = decode_text(simple_sub_cipher, encoded_text)
    assert text != encoded_text, "dependent on this particular cipher"
    assert encoded_text[0].upper() == encoded_text[0]
    assert text == decoded_text
