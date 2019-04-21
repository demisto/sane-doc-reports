import base64
import importlib
import re
from io import BytesIO

from PIL.Image import Image
from docx.shared import RGBColor


def hex_to_rgb(hex_color: str):
    """
    Convert a hex color string into an RGBColor object (used in python-docx)
    """
    hex_color = hex_color.lstrip('#')
    return RGBColor(*[int(hex_color[i:i + 2], 16) for i in (0, 2, 4)])


def open_b64_image(image_base64: str):
    """
    Open a virtual image file for base64 format of image.
    """
    prefix_regex = r'^data:.*?;base64,'
    raw_base64 = re.sub(prefix_regex, '', image_base64)
    f = BytesIO()
    f.write(base64.b64decode(raw_base64))
    f.seek(0)
    return f


def create_b64_image(image: Image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")

    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    return f'data:image/png;base64,{img_b64}'


def insert_by_type(type: str, cell_object: dict, section: dict):
    func = importlib.import_module(f'sane_doc_reports.docx.{type}')
    func.insert(cell_object, section)