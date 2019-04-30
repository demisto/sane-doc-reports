import base64
import re
from io import BytesIO, StringIO
import xml.etree.cElementTree as ET
import importlib

import mistune
from docx.oxml import OxmlElement
from docx.shared import RGBColor
from docx.text.paragraph import Paragraph
from lxml.html import soupparser

from sane_doc_reports import CellObject
from sane_doc_reports.markdown_utils import build_dict, collapse_attrs
from matplotlib import colors as mcolors

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


def markdown_to_list(markdown_string):
    """ Convert markdown to HTML->Python list,
        This will be a readable list of dicts containing:
            - Type: type of html element
            - Contents: text content or list of other dicts
            - Attrs (any defined sane_doc_reports.conf.HTML_ATTRIBUTES)

        For example:
        markdown = '**~~123~~**'
        -> <p><strong><strike>123</strike></strong></p>
        ->[
          {
            "type": "p",
            "attrs": ["strong","strike"],
            "contents": "123"
          }
        ]
    """
    html = mistune.markdown(markdown_string).strip()
    etree_root = soupparser.parse(StringIO(html)).getroot()
    html_list = list(map(build_dict, [c for c in list(etree_root)]))
    return collapse_attrs(html_list)


def insert_by_type(type: str, cell_object: CellObject, section: dict):
    """ Call a docx elemnt's insert method """
    func = importlib.import_module(f'sane_doc_reports.docx.{type}')
    func.invoke(cell_object, section)



def _insert_paragraph_after(paragraph):
    """Insert a new paragraph after the given paragraph."""
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)

    return new_para


def add_run(cell_object):
    """ Insert a paragraph so we could add a new element"""
    cell_object['paragraph'] = _insert_paragraph_after(cell_object['paragraph'])
    cell_object['run'] = cell_object['paragraph'].add_run()
    return cell_object
