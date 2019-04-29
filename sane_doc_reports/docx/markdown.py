from typing import Dict

from sane_doc_reports.conf import DEBUG, DATA_KEY, LAYOUT_KEY, STYLE_KEY
from sane_doc_reports.docx import text, md_hr, md_quote
from sane_doc_reports.style import apply_styling
from sane_doc_reports.utils import markdown_to_list, add_run


# TODO: move these to a transformers module?
def header(section):
    level = int(section['type'].replace('h', ''))
    computed_style = {"fontSize": 34 - level * 2}
    computed_style = {**computed_style, **section['attrs']}

    return {
        "type": "text",
        f'{DATA_KEY}': {
            "text": section['contents'],
        },
        f'{LAYOUT_KEY}': {
            f'{STYLE_KEY}': computed_style
        }
    }


def paragraph(section):
    computed_style = {**section['attrs']}
    if 'fontSize' not in computed_style:
        computed_style['fontSize'] = 14

    return {
        "type": "text",
        f'{DATA_KEY}': {
            "text": section['contents'],
        },
        f'{LAYOUT_KEY}': {
            f'{STYLE_KEY}': computed_style
        }
    }


def quote(cell_object, section):
    new_cell_object = md_quote.insert(cell_object, None)

    # I'm a genius, you need to clap now :)
    insert(new_cell_object, section['contents'], recursive=True)


def hr():
    return {
        "type": "md_hr"
    }


def fix_attrs(attrs):
    return {k: True for k in attrs}


def insert(cell_object: Dict, section: Dict, recursive=False) -> None:
    if DEBUG:
        print("Yo Im markdown chart")

    if not recursive:
        section_list = markdown_to_list(section[DATA_KEY]['text'])
    else:
        section_list = section

    for s in section_list:
        s['attrs'] = fix_attrs(s['attrs'])

        # H1 <> Header
        if s['type'] in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if not recursive:
                cell_object = add_run(cell_object)

            section = header(s)
            if STYLE_KEY in section[LAYOUT_KEY]:
                apply_styling(cell_object, section[LAYOUT_KEY][STYLE_KEY])

            text.insert(cell_object, section)
            continue

        # P <> Normal text
        if s['type'] == 'p':
            if not recursive:
                cell_object = add_run(cell_object)

            section = paragraph(s)
            if STYLE_KEY in section[LAYOUT_KEY]:
                apply_styling(cell_object, section[LAYOUT_KEY][STYLE_KEY])

            text.insert(cell_object, section)
            continue

        # Blockquote <> Quote
        if s['type'] == 'blockquote':
            cell_object = add_run(cell_object)
            quote(cell_object, s)
            continue

        # HR <> HorizontalLine
        if s['type'] == 'hr':
            if not recursive:
                cell_object = add_run(cell_object)
            cell_object = add_run(cell_object)  # Bug fix, for multiple hrs
            section = hr()
            md_hr.insert(cell_object, section)
            continue

        print(s['type'])
