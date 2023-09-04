from PIL import Image, ImageDraw, ImageFont


def write_text(text: str, size: int, xy: tuple[float, float], image: Image.Image) -> Image.Image:
    """Writes the input text at the coordinates xy."""
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/FreeMono.ttf", size)
    draw.text(xy, text, font=font, fill=(255, 255, 255))
    return image
