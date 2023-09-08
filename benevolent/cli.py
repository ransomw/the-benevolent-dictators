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
    """Exclusive or (xor) two images together"""
    with Image.open(path1) as image1, Image.open(path2) as image2:
        image_out = create_xor_code(image1, image2)
        image_out.save(path_out)


@cli.command()
@click.argument("image-path", required=True, type=click.Path(exists=True))
@click.argument("text", required=True, type=click.STRING)
@click.option("--size", required=True, type=click.IntRange(min=1))
@click.option("-x", required=True, type=click.IntRange(min=0))
@click.option("-y", required=True, type=click.IntRange(min=0))
@click.argument("path-out", required=True, type=click.Path(exists=False))
def box_write(image_path, text, size, x, y, path_out):
    """Write text to an image inside a box."""
    with Image.open(image_path) as image:
        writer = Writer(image, size)
        writer.write_text_box(text, (x, y))

        image.save(path_out)


@cli.command()
@click.argument("text", required=True, type=click.STRING)
@click.option("--cipher-path", required=False, type=click.Path(exists=True))
@click.option("--cipher-seed", required=False)
def encode_with_cipher(text, cipher_path, cipher_seed):
    """Encodes some text with the given cipher."""
    if not cipher_path and not cipher_seed:
        raise ValueError("Either a path or a seed for the cipher is needed.")
    if cipher_path and cipher_seed:
        raise ValueError("Either select a path to the cipher OR a seed to the cipher.")

    if cipher_path:
        sub_cipher = sc.load_simple_sub_cipher(Path(cipher_path))
    if cipher_seed:
        sub_cipher = sc.generate_seeded_sub_cipher(cipher_seed)

    click.echo(sc.encode_simple_sub_cipher(sub_cipher, text))


@cli.command()
@click.argument("encoded-text", required=True, type=click.STRING)
@click.option("--cipher-path", required=False, type=click.Path(exists=True))
@click.option("--cipher-seed", required=False)
def decode_with_cipher(encoded_text, cipher_path, cipher_seed):
    """Decodes some text with the given cipher."""
    if not cipher_path and not cipher_seed:
        raise ValueError("Either a path or a seed for the cipher is needed.")
    if cipher_path and cipher_seed:
        raise ValueError("Either select a path to the cipher OR a seed to the cipher.")

    if cipher_path:
        sub_cipher = sc.load_simple_sub_cipher(Path(cipher_path))
    if cipher_seed:
        sub_cipher = sc.generate_seeded_sub_cipher(cipher_seed)

    click.echo(sc.decode_simple_sub_cipher(sub_cipher, encoded_text))


@cli.command()
@click.argument("cipher-path", required=True, type=click.Path(exists=False, dir_okay=False))
@click.option("--cipher-seed", required=False)
def generate_cipher(cipher_path, cipher_seed=None):
    """Generates a new cipher file."""
    if cipher_seed:
        sub_cipher = sc.generate_seeded_sub_cipher(cipher_seed)
    else:
        sub_cipher = sc.generate_simple_sub_cipher()
    sc.save_simple_sub_cipher(sub_cipher, Path(cipher_path))


@cli.command()
@click.argument("image-path-in", required=True, type=click.Path(exists=True))
@click.option("--cipher-path", required=False, type=click.Path(exists=True))
@click.option("--cipher-seed", required=False)
@click.option("--format", required=False)
@click.argument("image-path-out", required=True, type=click.Path(exists=False))
def benevolens(image_path_in, cipher_path, cipher_seed, format, image_path_out):
    """Reads text from an image and decodes it.

     image-path-in: The path where the image you want to decode is.
     --cipher-path: The path for the cipher file to use for decoding.
     --cipher-seed: The cipher seed to use for decoding.
          --format: valid PIL bitmap format.
    image-path-out: The path to save the decoded image in.
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
        cipher = sc.load_simple_sub_cipher(Path(cipher_path))

    return cipher
