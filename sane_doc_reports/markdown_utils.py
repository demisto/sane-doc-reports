from io import StringIO
from typing import List

import mistune
from lxml.html import soupparser

from sane_doc_reports.MarkdownSection import MarkdownSection
from sane_doc_reports.conf import HTML_ATTRIBUTES


def collapse_attrs(section_list):
    ret = []
    for section in section_list:
        s = MarkdownSection(section['type'], section['contents'],
                            section['layout'], section['extra'])
        s.collapse(False)
        ret.append(s)
    return ret


def build_dict(elem):
    children = list(elem)
    has_children = len(children) > 0
    elem_text = elem.text if elem.text else ''

    contents = elem_text.strip()

    if has_children:
        contents = list(map(build_dict, children))

    extra = {}
    if 'src' in elem.attrib:
        extra['src'] = elem.attrib['src']

    return {'type': elem.tag, 'attrs': [], 'layout': {}, 'contents': contents,
            'extra': extra}

