from typing import Dict

import mistune

from sane_doc_reports.conf import DEBUG, DOMAIN, DATA_KEY, LAYOUT_KEY, STYLE_KEY
from sane_doc_reports.docx import text


class DocxRenderer(mistune.Renderer):
    """
    We need a renderer class like this so mistune will parse the markdown for
    us and we could change the output.
    Here we generate JSON (like sane's JSON) that we will later send to the
    other docx elements. (Yeah it's kind of a hack of the renderer)
    """
    cell_object = None

    def attach_sane_constructor(self):
        # A small hack to inject the cell reference so it can be used here.
        self.sane = []

    def double_emphasis(self, text_value):
        return f"__bold__{text_value}"

    def header(self, text_value, level, raw=None):
        bold = False
        if '__bold__' in text_value:
            bold = True
            text_value = text_value.replace('__bold__', '')

        font_size = 30 - level * 2
        section = {
            f'{DATA_KEY}': {
                'text': text_value
            },
            f'{LAYOUT_KEY}': {
                f'{STYLE_KEY}': {
                    'name': 'Arial',
                    'fontSize': font_size,
                    'color': 'black',
                    'textAlign': 'left',
                    'bold': bold
                }
            }
        }
        self.sane.append(section)
        return ''

    def paragraph(self, text_value):
        section = {
            f'{DATA_KEY}': {
                'text': text_value
            },
            f'{LAYOUT_KEY}': {
                f'{STYLE_KEY}': {
                    'name': 'Arial',
                    'fontSize': 14,
                    'color': '#6c6c6c',
                    'textAlign': 'left'
                }
            }
        }
        self.sane.append(section)
        return ''


def insert_from_markdowm(cell_object: dict, markdown_string: str) -> None:
    renderer = DocxRenderer()
    renderer.attach_sane_constructor()

    markdown = mistune.Markdown(renderer=renderer)
    markdown(markdown_string)

    is_first = True
    # We need to reverse the sane list because adding paragraphs is adding them
    # before and not after (python-docx).
    for elem in markdown.renderer.sane[::-1]:
        text.insert(cell_object, elem, is_first)
        is_first = False


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo Im markdown")

    markdown_string = section[DATA_KEY]['text']
    insert_from_markdowm(cell_object, markdown_string)
