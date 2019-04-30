import base64
import re
import tempfile
from io import BytesIO
import importlib
from pathlib import Path

import matplotlib
from docx.shared import RGBColor

from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

from sane_doc_reports.conf import LAYOUT_KEY

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


def name_to_rgb(color_name: str):
    hex_color = name_to_hex(color_name)
    return hex_to_rgb(hex_color)


def name_to_hex(color_name: str):
    """ Get the hex representation of a color name (CSS4) """
    return colors[color_name]


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
    prefix_regex = r'^data:.*?;base64,'
    raw_base64 = re.sub(prefix_regex, '', image_base64)
    f = BytesIO()
    f.write(base64.b64decode(raw_base64))
    f.seek(0)
    return f


def insert_by_type(type: str, cell_object: dict, section: dict):
    """ Call a docx elemnt's insert method """
    func = importlib.import_module(f'sane_doc_reports.docx.{type}')
    func.insert(cell_object, section)


def plot(func):
    """ A decorator used to clear and resize each chart """

    def wrapper(*args, **kwargs):
        plt.clf()
        func(*args, **kwargs)

    return wrapper


def plt_t0_b64(plt: matplotlib.pyplot):
    """ Matplotlib to base64 url """
    path = Path(tempfile.mkdtemp()) / Path(
        next(tempfile._get_candidate_names()) + '.png')

    plt.savefig(str(path), format='png', bbox_inches='tight', figsize=(1, 1),
                dpi=80)

    with open(str(path), "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8", "ignore")
        b64 = f'data:image/png;base64,{img_base64}'

    path.unlink()
    return b64


def get_plt_size(section):
    size_w, size_h, dpi = (6, 3, 80)
    if 'dimensions' in section[LAYOUT_KEY]:
        h = section[LAYOUT_KEY]['dimensions']['height'] / 100.0
        w = section[LAYOUT_KEY]['dimensions']['width'] / 100.0
        size_w, size_h, dpi = (w, h, 100)
    return size_w, size_h, dpi


def get_saturated_colors():
    """ Return named colors that are clearly visible on a white background """
    return [name for name, _ in colors.items()
            if 'light' not in name and 'white' not in name]
