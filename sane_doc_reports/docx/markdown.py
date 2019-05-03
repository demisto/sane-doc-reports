from typing import Dict

from sane_doc_reports import CellObject, Section
from sane_doc_reports.Wrapper import Wrapper


class MarkdownWrapper(Wrapper):

    def wrap(self):
        print("Wrapping markdown")


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
