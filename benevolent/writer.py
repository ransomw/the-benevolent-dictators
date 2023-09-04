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
        self.font = ImageFont.truetype("fonts/FreeMono.ttf", text_size)

    def write_text_box(self, text: str, xy: tuple[float, float]) -> None:
        """Write text inside a box."""
        self.draw.rectangle(self.draw.textbbox(xy, text, self.font), fill=(0, 0, 0), outline=(0, 0, 0))

        self.write_text(text, xy)

    def write_text(self, text: str, xy: tuple[float, float]) -> None:
        """Write the input text at the coordinates xy."""
        self.draw.text(xy, text, font=self.font, fill=(255, 255, 255))
