import base64
import re
import tempfile
from io import BytesIO
import importlib
from pathlib import Path

from docx.oxml import OxmlElement
import matplotlib
from docx.shared import RGBColor, Pt
from docx.text.paragraph import Paragraph
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

from sane_doc_reports import CellObject, Section
from sane_doc_reports.conf import SIZE_H_INCHES, SIZE_W_INCHES, DPI, STYLE_KEY

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


def name_to_rgb(color_name: str):
    hex_color = name_to_hex(color_name)
    return hex_to_rgb(hex_color)


def name_to_hex(color_name: str):
    """ Get the hex representation of a color name (CSS4) """
    return colors[color_name].lower()


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


def insert_by_type(type: str, cell_object: CellObject,
                   section: Section):
    """ Call a docx elemnt's insert method """
    func = importlib.import_module(f'sane_doc_reports.docx.{type}')

    if section.layout:
        apply_styling(cell_object, section.layout[STYLE_KEY])

    func.invoke(cell_object, section)


def _insert_paragraph_after(paragraph):
    """Insert a new paragraph after the given paragraph."""
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)

    return new_para


def add_run(cell_object):
    """ Insert a paragraph so we could add a new element"""
    cell_object.paragraph = _insert_paragraph_after(cell_object.paragraph)
    cell_object.run = cell_object.paragraph.add_run()
    return cell_object


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


def convert_plt_size(section: Section):
    """ Convert the plot size from pixels to word """
    size_w, size_h, dpi = (SIZE_W_INCHES, SIZE_H_INCHES, DPI)
    if 'dimensions' in section.layout:
        h = section.layout['dimensions']['height'] / 100.0
        w = section.layout['dimensions']['width'] / 100.0
        size_w, size_h, dpi = (w, h, 100)
    return size_w, size_h, dpi


def get_saturated_colors():
    """ Return named colors that are clearly visible on a white background """
    return [name for name, _ in colors.items()
            if 'light' not in name and 'white' not in name]


def apply_styling(cell_object, style):
    apply_cell_styling(cell_object, style)
    apply_paragraph_styling(cell_object, style)


def apply_cell_styling(cell_object, style):
    # Font size
    if 'fontSize' in style:
        cell_object.run.font.size = Pt(style['fontSize'])

    # Font family
    if 'name' in style:
        cell_object.run.font.name = style['name']

    # Other characteristics
    if 'bold' in style:
        cell_object.run.font.bold = style['bold']
    if 'strikethrough' in style:
        cell_object.run.font.strike = style['strikethrough']
    if 'underline' in style:
        cell_object.run.font.underline = style['underline']
    if 'italic' in style:
        cell_object.run.font.italic = style['italic']

    # Font color
    if 'color' in style:
        if style['color'][0] != '#':
            cell_object.run.font.color.rgb = name_to_rgb(style['color'])
        else:
            cell_object.run.font.color.rgb = hex_to_rgb(style['color'])


def apply_paragraph_styling(cell_object, style):
    if 'textAlign' in style:
        # text align
        if style['textAlign'] == 'left':
            # cell.alignment = 0
            cell_object.paragraph.paragraph_format.alignment = 0
        elif style['textAlign'] == 'right':
            # cell.alignment = 1
            cell_object.paragraph.paragraph_format.alignment = 2
