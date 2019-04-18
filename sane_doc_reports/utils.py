import base64
from io import BytesIO

from docx.shared import RGBColor


def hex_to_rgb(hex_color: str):
    """
    Convert a hex color string into an RGBColor object (used in python-docx)
    """
    hex_color = hex_color.lstrip('#')
    return RGBColor(*[int(hex_color[i:i + 2], 16) for i in (0, 2, 4)])


def open_b64_image(image_base64):
    """
    Open a virtual image file for base64 format of image.
    """
    raw_base64 = image_base64[image_base64.index(";base64,") + 8:]
    f = BytesIO()
    f.write(base64.b64decode(raw_base64))
    f.seek(0)
    return f
