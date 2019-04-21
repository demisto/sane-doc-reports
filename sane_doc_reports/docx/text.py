from typing import Dict

from sane_doc_reports.conf import LAYOUT_KEY, STYLE_KEY, DATA_KEY
from sane_doc_reports.utils import hex_to_rgb
from docx.shared import Pt
import webcolors


def insert(cell_object: Dict, section: Dict) -> None:
    cell = cell_object['run']
    paragraph = cell_object['paragraph']

    cell.text = section[DATA_KEY]['text']

    if STYLE_KEY not in section[LAYOUT_KEY]:
        return

    style = section[LAYOUT_KEY][STYLE_KEY]
    font = cell.font

    # Font size
    if 'fontSize' in style:
        font.size = Pt(style['fontSize'])

    # Font family
    if 'name' in style:
        font.name = style['name']

    # Other characteristics
    if 'bold' in style:
        font.bold = style['bold']
    if 'strikethrough' in style:
        font.strike = style['strikethrough']

    # Font color
    if 'color' in style:
        if style['color'][0] != '#':
            font.color.rgb = hex_to_rgb(webcolors.name_to_hex(style['color']))
        else:
            font.color.rgb = hex_to_rgb(style['color'])

    # text align
    if style['textAlign'] == 'left':
        cell.alignment = 0
        paragraph.paragraph_format.alignment = 0
    elif style['textAlign'] == 'right':
        cell.alignment = 1
        paragraph.paragraph_format.alignment = 2
