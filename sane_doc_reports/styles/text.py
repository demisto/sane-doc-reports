from sane_doc_reports.conf import STYLE_KEY
from sane_doc_reports.utils import apply_styling


def apply_style(cell_object, section):
    computed_style = {"fontSize": 14}
    attached_styles = {k: True for k in section.attrs}
    computed_style = {**computed_style, **attached_styles}

    section.layout[STYLE_KEY] = computed_style

    if section.layout and STYLE_KEY in section.layout:
        apply_styling(cell_object, section.layout[STYLE_KEY])
