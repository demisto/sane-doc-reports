from typing import Dict

from sane_doc_reports import CellObject, Section
from sane_doc_reports.MarkdownSection import markdown_to_section_list
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.docx import text
from sane_doc_reports.styles import header


class MarkdownWrapper(Wrapper):

    def wrap(self):

        md_section_ist = markdown_to_section_list(self.section.contents)

        if not isinstance(md_section_ist, list):
            raise ValueError('Markdown section does not have valid contents ' +
                             '(must be a list)')

        for section in md_section_ist:

            section_type = section.type

            if section_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                header.apply_style(self.cell_object, section)
                text.invoke(self.cell_object, section)
                continue

            if section_type in ['p']:
                # Call text.invoke with normal styling
                continue

            if section_type == 'a':
                # Call link.invoke with normal styling
                continue

            if section_type == 'pre':
                # Call md_code.invoke
                continue

            if section_type == 'blockquote':
                # Call md_quote.invoke
                continue

            if section_type == 'hr':
                # Call md_hr.invoke
                continue

            if section_type == 'ul':
                # Call md_ul.invoke
                continue

            if section_type == 'ol':
                # Call md_ol.invoke
                continue

            if section_type == 'li':
                # Call md_li.invoke
                continue

            raise ValueError(f'Section type is not defined: {section_type}')


def invoke(cell_object: CellObject, section: Section):
    if section.type != 'markdown':
        raise ValueError('Called markdown but not markdown - ', section)

    MarkdownWrapper(cell_object, section).wrap()

# # TODO: move these to a transformers module?
# def header(section):
#     level = int(section['type'].replace('h', ''))
#     computed_style = {"fontSize": 34 - level * 2}
#     computed_style = {**computed_style, **section['attrs']}
#
#     return {
#         "type": "text",
#         f'{DATA_KEY}': {
#             "text": section['contents'],
#         },
#         f'{LAYOUT_KEY}': {
#             f'{STYLE_KEY}': computed_style
#         }
#     }
#
#
# def paragraph(section):
#     computed_style = {**section['attrs']}
#     if 'fontSize' not in computed_style:
#         computed_style['fontSize'] = 14
#
#     return {
#         "type": "text",
#         f'{DATA_KEY}': {
#             "text": section['contents'],
#         },
#         f'{LAYOUT_KEY}': {
#             f'{STYLE_KEY}': computed_style
#         }
#     }
#
#
# def quote(cell_object, section):
#     new_cell_object = md_quote.insert(cell_object, None)
#
#     insert(new_cell_object, section['contents'], recursive=True)
#
#
# def code(cell_object, section):
#     if isinstance(section, dict) and section['type'] == 'code':
#         insert(cell_object, section, recursive=True)
#         return
#
#     new_cell_object = md_code.insert(cell_object, None)
#     insert(new_cell_object, section['contents'], recursive=True)
#
#
# def hr():
#     return {
#         "type": "md_hr"
#     }
#
#
# def fix_attrs(attrs):
#     return {k: True for k in attrs}
#
#
# def insert(cell_object: Dict, section: Dict, recursive=False, meta={}) -> None:
#     """
#
#     :param cell_object:
#     :param section:
#     :param recursive: if we should create a new paragraph / run
#     :param meta:
#     :return:
#     """
#     if DEBUG:
#         print("Yo Im markdown chart")
#
#     if not recursive:
#         section_list = markdown_to_list(section[DATA_KEY]['text'])
#     else:
#         section_list = section
#
#     for s in section_list:
#         s['attrs'] = fix_attrs(s['attrs'])
#
#         # H1 <> Header
#         if s['type'] in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
#             if not recursive:
#                 cell_object = add_run(cell_object)
#
#             section = header(s)
#             if STYLE_KEY in section[LAYOUT_KEY]:
#                 apply_styling(cell_object, section[LAYOUT_KEY][STYLE_KEY])
#
#             text.insert(cell_object, section)
#             continue
#
#         # P <> Normal text
#         if s['type'] in ['p', 'code']:
#             if not recursive:
#                 cell_object = add_run(cell_object)
#
#             section = paragraph(s)
#             if STYLE_KEY in section[LAYOUT_KEY]:
#                 apply_styling(cell_object, section[LAYOUT_KEY][STYLE_KEY])
#
#             print(section)
#             text.insert(cell_object, section)
#             continue
#
#         # Pre <> Code
#         if s['type'] in 'pre':
#             cell_object = add_run(cell_object)
#             code(cell_object, s)
#             continue
#
#         # Blockquote <> Quote
#         if s['type'] == 'blockquote':
#             cell_object = add_run(cell_object)
#             quote(cell_object, s)
#             continue
#
#         # HR <> HorizontalLine
#         if s['type'] == 'hr':
#             if not recursive:
#                 cell_object = add_run(cell_object)
#             cell_object = add_run(cell_object)  # Bug fix, for multiple hrs
#             section = hr()
#             md_hr.insert(cell_object, section)
#             continue
#
#         print(s['type'])
