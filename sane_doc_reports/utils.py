import base64
import re
from io import BytesIO
import xml.etree.cElementTree as ET

import mistune
from docx.shared import RGBColor

from sane_doc_reports.markdown_utils import build_dict, collapse_attrs


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

    # Etree needs a wrapping element to function correctly
    fixed_html = f'<root>{html}</root>'
    etree_root = ET.fromstring(fixed_html)
    html_list = list(map(build_dict, [c for c in list(etree_root)]))
    return collapse_attrs(html_list)
