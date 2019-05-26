from docx.shared import Pt

from sane_doc_reports.conf import PYDOCX_FONT_SIZE, PYDOCX_FONT_NAME, \
    PYDOCX_FONT_BOLD, PYDOCX_FONT_STRIKE, PYDOCX_FONT_UNDERLINE, \
    PYDOCX_FONT_ITALIC, PYDOCX_FONT_COLOR, PYDOCX_TEXT_ALIGN, DEFAULT_WORD_FONT
from sane_doc_reports.styles.colors import name_to_rgb, hex_to_rgb


def apply_styling(cell_object, style):
    apply_cell_styling(cell_object, style)
    apply_paragraph_styling(cell_object, style)


def apply_cell_styling(cell_object, style):
    if "HIGHLIGHT" in style:
        print("woiwoowow")

    # Font size
    if PYDOCX_FONT_SIZE in style:
        cell_object.run.font.size = Pt(style[PYDOCX_FONT_SIZE])

    # Set default font
    cell_object.run.font.name = DEFAULT_WORD_FONT

    # Font family
    if PYDOCX_FONT_NAME in style:
        cell_object.run.font.name = style[PYDOCX_FONT_NAME]

    # Other characteristics
    if PYDOCX_FONT_BOLD in style:
        cell_object.run.font.bold = style[PYDOCX_FONT_BOLD]
    if PYDOCX_FONT_STRIKE in style:
        cell_object.run.font.strike = style[PYDOCX_FONT_STRIKE]
    if PYDOCX_FONT_UNDERLINE in style:
        cell_object.run.font.underline = style[PYDOCX_FONT_UNDERLINE]
    if PYDOCX_FONT_ITALIC in style:
        cell_object.run.font.italic = style[PYDOCX_FONT_ITALIC]

    # Font color
    if PYDOCX_FONT_COLOR in style:
        if style[PYDOCX_FONT_COLOR][0] != '#':
            cell_object.run.font.color.rgb = name_to_rgb(
                style[PYDOCX_FONT_COLOR])
        else:
            cell_object.run.font.color.rgb = hex_to_rgb(
                style[PYDOCX_FONT_COLOR])


def apply_paragraph_styling(cell_object, style):
    if PYDOCX_TEXT_ALIGN in style:
        if style[PYDOCX_TEXT_ALIGN] == 'left':
            cell_object.paragraph.paragraph_format.alignment = 0
        elif style[PYDOCX_TEXT_ALIGN] == 'right':
            cell_object.paragraph.paragraph_format.alignment = 2
        elif style[PYDOCX_TEXT_ALIGN] == 'center':
            cell_object.paragraph.paragraph_format.alignment = 1
