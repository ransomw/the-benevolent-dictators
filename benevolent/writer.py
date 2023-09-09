from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class Writer:
    """Allows writing text inside an image."""

    def __init__(self, image: Image.Image, text_size: int) -> None:
        """Create a Writer object.

        inputs:
            - image: The image that text will be written on.
            - text_size: The size of the text that will be written.
        """
        self.draw = ImageDraw.Draw(image)
        font_path = str((Path("fonts") / "FreeMono.ttf").absolute())
        self.font = ImageFont.truetype(font_path, text_size)

    def write_text_box(self, text: str, xy: tuple[float, float]) -> None:
        """Write text inside a box."""
        self.draw_box(self.draw.textbbox(xy, text, self.font))

        self.write_text(text, xy)

    def draw_box(self, bounding_box) -> None:
        """Draw a black box."""
        self.draw.rectangle(bounding_box, fill=(255, 255, 255), outline=(255, 255, 255))

    def write_text(self, text: str, xy: tuple[float, float]) -> None:
        """Write the input text at the coordinates xy."""
        self.draw.text(xy, text, font=self.font, fill=(0, 0, 0))
