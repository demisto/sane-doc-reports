from typing import Dict

from sane_doc_reports.conf import DEBUG, DATA_KEY, LAYOUT_KEY, STYLE_KEY
from sane_doc_reports.docx import text
from sane_doc_reports.style import apply_styling
from sane_doc_reports.utils import markdown_to_list, add_run


def header(section):
    level = int(section['type'].replace('h', ''))
    computed_style = {"fontSize": 34 - level * 2}
    if STYLE_KEY in section:
        computed_style = {**computed_style, **section[STYLE_KEY]}
    return {
        "type": "text",
        f'{DATA_KEY}': {
            "text": section['contents'],
        },
        f'{LAYOUT_KEY}': {
            f'{STYLE_KEY}': computed_style
        }
    }


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo Im markdown chart")

    section_list = markdown_to_list(section[DATA_KEY]['text'])
    for s in section_list:
        if s['type'] in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            cell_object = add_run(cell_object)

            section = header(s)
            if STYLE_KEY in section[LAYOUT_KEY]:
                apply_styling(cell_object, section[LAYOUT_KEY][STYLE_KEY])

            text.insert(cell_object, section)
            continue
