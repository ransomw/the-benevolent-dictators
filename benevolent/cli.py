import click
from PIL import Image

from benevolent.xor_enconder import create_xor_code

@click.group()
def cli():
    """command-line interface root"""
    pass

@cli.command()
@click.option("--path1", required=True, type=click.Path(exists=True))
@click.option("--path2", required=True, type=click.Path(exists=True))
@click.option("--path-out", required=True, type=click.Path(exists=False))
def xor_code(path1, path2, path_out):
    """xor two images together and store them as an output image"""
    with Image.open(path1) as image1, Image.open(path2) as image2:
        image_out = create_xor_code(image1, image2)
        image_out.save(path_out)

