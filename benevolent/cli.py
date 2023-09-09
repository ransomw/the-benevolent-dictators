from pathlib import Path

import click
from PIL import Image

import benevolent.sub_cipher as sc
from benevolent.conf import config_file_path
from benevolent.translator import translate_image
from benevolent.writer import Writer
from benevolent.xor_enconder import create_xor_code


@click.group()
def cli():
    """Command-line interface root"""
    pass


@cli.command()
def print_config_path():
    """Print the location of the config file to stdout"""
    path = config_file_path()
    click.echo(f"{path}")


@cli.command()
@click.argument("path1", required=True, type=click.Path(exists=True))
@click.argument("path2", required=True, type=click.Path(exists=True))
@click.argument("path-out", required=True, type=click.Path(exists=False))
def xor_code(path1, path2, path_out):
    """Exclusive or (xor) two images together

    path1 is the path of the first image to use.
    path2 is the path of the second image to use.
    path-out is the path where the resulting image will be saved.
    """
    with Image.open(path1) as image1, Image.open(path2) as image2:
        image_out = create_xor_code(image1, image2)
        image_out.save(path_out)


@cli.command()
@click.argument("image-path", required=True, type=click.Path(exists=True))
@click.argument("text", required=True, type=click.STRING)
@click.option("--size", required=True, type=click.IntRange(min=1), help="Size of the text font.")
@click.option("-x", required=True, type=click.IntRange(min=0), help="x position to write in.")
@click.option("-y", required=True, type=click.IntRange(min=0), help="x position to write in.")
@click.argument("path-out", required=True, type=click.Path(exists=False))
def box_write(image_path, text, size, x, y, path_out):
    """Write text to an image inside a box.

    image-path is the path of the image that will be written in.
    text is the text to write.
    path-out is the path to save the image with the written text to.
    """
    with Image.open(image_path) as image:
        writer = Writer(image, size)
        writer.write_text_box(text, (x, y))

        image.save(path_out)


@cli.command()
@click.argument("text", required=True, type=click.STRING)
@click.option("--cipher-path", required=False, type=click.Path(exists=True),
              help="Path where the cipher to use is, when encoding with one.")
@click.option("--cipher-seed", required=False, help="Seed to use to encode the text, when encoding with one.")
def encode_with_cipher(text, cipher_path, cipher_seed):
    """Encodes some text with the given cipher. Either provide the path to a cipher file or a seed."""
    if not cipher_path and not cipher_seed:
        raise ValueError("Either a path or a seed for the cipher is needed.")
    if cipher_path and cipher_seed:
        raise ValueError("Either select a path to the cipher OR a seed to the cipher.")

    if cipher_path:
        sub_cipher = sc.load_cipher(Path(cipher_path))
    if cipher_seed:
        sub_cipher = sc.generate_seeded_sub_cipher(cipher_seed)

    click.echo(sc.encode_text(sub_cipher, text))


@cli.command()
@click.argument("encoded-text", required=True, type=click.STRING)
@click.option("--cipher-path", required=False, type=click.Path(exists=True),
              help="Path where the cipher to use is, when decoding with one.")
@click.option("--cipher-seed", required=False, help="Seed to decode the text with, when decoding with one.")
def decode_with_cipher(encoded_text, cipher_path, cipher_seed):
    """Decodes some text with the given cipher. Either provide the path to a cipher file or a seed."""
    if not cipher_path and not cipher_seed:
        raise ValueError("Either a path or a seed for the cipher is needed.")
    if cipher_path and cipher_seed:
        raise ValueError("Either select a path to the cipher OR a seed to the cipher.")

    if cipher_path:
        sub_cipher = sc.load_cipher(Path(cipher_path))
    if cipher_seed:
        sub_cipher = sc.generate_seeded_sub_cipher(cipher_seed)

    click.echo(sc.decode_text(sub_cipher, encoded_text))


@cli.command()
@click.argument("cipher-path", required=True, type=click.Path(exists=False, dir_okay=False))
@click.option("--cipher-seed", required=False, help="(Optional) Seed to use to generate the cipher.")
def generate_cipher(cipher_path, cipher_seed=None):
    """Generates a new cipher file.

    cipher-path is the path where the generated file will be saved to.
    """
    if cipher_seed:
        sub_cipher = sc.generate_seeded_sub_cipher(cipher_seed)
    else:
        sub_cipher = sc.generate_simple_sub_cipher()
    sc.save_cipher(sub_cipher, Path(cipher_path))


@cli.command()
@click.argument("image-path-in", required=True, type=click.Path(exists=True))
@click.option("--cipher-path", required=False, type=click.Path(exists=True),
              help="The path where the cipher file is located, when decoding with one.")
@click.option("--cipher-seed", required=False, help="The seed to use for decoding, when decoding with one.")
@click.option("--format", required=False, help="Valid PIL bitmap format.")
@click.argument("image-path-out", required=True, type=click.Path(exists=False))
def benevolens(image_path_in, cipher_path, cipher_seed, format, image_path_out):
    """Reads text from an image and decodes it. Either provide a cipher file path or a cipher seed.

    image-path-in is the path where the image you want to decode is.
    image-path-out the path to save the decoded image in.
    """
    img = Image.open(image_path_in)

    translated_image = translate_image(img, _get_cipher(cipher_path, cipher_seed))
    if format:
        translated_image.save(image_path_out, bitmap_format=[format])
    else:
        translated_image.save(image_path_out)


def _get_cipher(cipher_path, cipher_seed) -> sc.SimpleSubCipher:
    if not cipher_path and not cipher_seed:
        raise ValueError("Cipher or cipher seed needed for decoding.")
    if cipher_path and cipher_seed:
        raise ValueError("Either give a cipher to decode the string OR a seed to generate the cipher.")
    if cipher_seed:
        click.echo(cipher_seed)
        cipher = sc.generate_seeded_sub_cipher(cipher_seed)
    if cipher_path:
        click.echo(cipher_path)
        cipher = sc.load_cipher(Path(cipher_path))

    return cipher
