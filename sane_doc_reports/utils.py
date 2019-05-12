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

from sane_doc_reports.conf import LAYOUT_KEY, SIZE_H_INCHES, SIZE_W_INCHES, DPI

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
DEFAULT_BAR_COLOR = '#999999'
CHART_COLORS = ['#E57373', '#FF1D1E', '#FF5000', '#E55100', '#D74315',
                '#F06292', '#FF3F81', '#F50057', '#C2195B', '#E91D63',
                '#AD1457', '#CE93D8', '#EA80FC', '#FA99D0', '#FD5BDE',
                '#D500F9', '#AA00FF', '#BA68C8', '#B287FE', '#9575CD',
                '#AB47BC', '#8E24AA', '#8052F3', '#9FA8DA', '#7C71F5',
                '#536DFE', '#5C6BC0', '#3F51B5', '#6200EA', '#A3C9FF',
                '#64B5F6', '#03B0FF', '#2196F3', '#2979FF', '#295AFF',
                '#B7E7FF', '#81D4FA', '#80DEEA', '#00B8D4', '#039BE5',
                '#0277BD', '#1AEADE', '#18DEE5', '#00E5FF', '#4DD0E1',
                '#4DB6AC', '#0097A7', '#0097A7', '#64DC17', '#00E676',
                '#00C853', '#20B358', '#4CAF50', '#C5FE01', '#ADE901',
                '#50EB07', '#AED581', '#8BC34A', '#69A636', '#EDFE41',
                '#FFEA00', '#FFD740', '#F9A825', '#FB8C00', '#FF7500',
                '#DBDBDB', '#CFD8DC', '#9EB6C3', '#B2B7B9', '#989898',
                '#90A4AE']


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


def convert_plt_size(section):
    """ Convert the plot size from pixels to word """
    size_w, size_h, dpi = (SIZE_W_INCHES, SIZE_H_INCHES, DPI)
    if 'dimensions' in section[LAYOUT_KEY]:
        h = section[LAYOUT_KEY]['dimensions']['height'] / 100.0
        w = section[LAYOUT_KEY]['dimensions']['width'] / 100.0
        size_w, size_h, dpi = (w, h, 100)

    return size_w, size_h, dpi


def _hash_simple_value(string):
    str_value = '' + string
    hash_value = 5381
    i = len(str_value)

    while i > 1:
        i = i - 1
        hash_value = (hash_value * 33) ^ ord(str_value[i])

    return hash_value


def _hash_string(list_or_value):
    if not list_or_value:
        return list_or_value

    if isinstance(list_or_value, list):
        return list(map(list_or_value, _hash_string))

    return _hash_simple_value(list_or_value)


def get_chart_color(value):
    """ Trying to copy the sane-report color scheme """
    if not value:
        return DEFAULT_BAR_COLOR

    index = _hash_string(value) % len(CHART_COLORS)
    return CHART_COLORS[index]
