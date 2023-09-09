from PIL import Image

from benevolent.sub_cipher import SimpleSubCipher
from benevolent.translator import translate_image


def translate_chunks(image: Image.Image,
                     cipher: SimpleSubCipher,
                     chunks: list[tuple[int, int, int, int]]
                     ) -> Image.Image:
    """Translate images in chunks, to hopefully increase tesseract accuracy."""
    image_out = image.copy()
    for chunk in chunks:
        translated_chunk = translate_image(image.crop(chunk), cipher)
        image_out.paste(translated_chunk, chunk)
    return image_out
