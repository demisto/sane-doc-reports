from sane_doc_reports.conf import STYLE_KEY
from sane_doc_reports.styles.utils import apply_styling


def apply_style(cell_object, section):
    """ Apply header specific styles and then the default style """
    level = int(section.type.replace('h', ''))
    pre_defined_styles = {}
    if STYLE_KEY in section.layout:
        pre_defined_styles = section.layout[STYLE_KEY]
    computed_style = {"fontSize": 36 - level * 2}
    attached_styles = {k: True for k in section.attrs}
    computed_style = {**computed_style, **attached_styles}

    section.layout[STYLE_KEY] = {**computed_style, **pre_defined_styles}

    if section.layout and STYLE_KEY in section.layout:
        apply_styling(cell_object, section.layout[STYLE_KEY])
