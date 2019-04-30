from docx.shared import Pt

from sane_doc_reports.utils import name_to_rgb, hex_to_rgb


def apply_styling(cell_object, style):
    apply_cell_styling(cell_object.run, style)
    apply_paragraph_styling(cell_object.paragraph, style)


def apply_cell_styling(run, style):
    font = run.font

    # Font size
    if 'fontSize' in style:
        font.size = Pt(style['fontSize'])

    # Font family
    if 'name' in style:
        font.name = style['name']

    # Other characteristics
    if 'bold' in style:
        font.bold = style['bold']
    if 'strikethrough' in style:
        font.strike = style['strikethrough']
    if 'underline' in style:
        font.underline = style['underline']
    if 'italic' in style:
        font.italic = style['italic']

    # Font color
    if 'color' in style:
        if style['color'][0] != '#':
            font.color.rgb = name_to_rgb(style['color'])
        else:
            font.color.rgb = hex_to_rgb(style['color'])


def apply_paragraph_styling(paragraph, style):

    if 'textAlign' in style:
        # text align
        if style['textAlign'] == 'left':
            # cell.alignment = 0
            paragraph.paragraph_format.alignment = 0
        elif style['textAlign'] == 'right':
            # cell.alignment = 1
            paragraph.paragraph_format.alignment = 2
