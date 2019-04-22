from typing import Dict

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt

from sane_doc_reports.conf import DEBUG, DATA_KEY
from sane_doc_reports.grid import get_cell_wrappers


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am a number")

    table = cell_object['cell'].add_table(rows=1, cols=1)

    # Add the main number
    inner_cell = table.cell(0, 0)
    inner_cell_paragraph, inner_cell_run = get_cell_wrappers(inner_cell)
    inner_cell_run.text = str(section[f'{DATA_KEY}'])
    inner_cell_run.font.size = Pt(24)
    inner_cell_run.font.bold = True
    inner_cell_paragraph.alignment = 1

    # Add the second number
    inner_2nd_paragraph = inner_cell.add_paragraph()
    inner_2nd_run = inner_2nd_paragraph.add_run()
    inner_2nd_run.text = str(section['title'])
    inner_2nd_run.font.size = Pt(14)
    inner_2nd_run.font.bold = False
    inner_2nd_paragraph.alignment = 1

    # Add background color
    color_str = 'f3f3f3'
    shading_elm_1 = parse_xml(
        (r'<w:shd {} w:fill="' + color_str + '"/>').format(nsdecls('w')))
    inner_cell._tc.get_or_add_tcPr().append(shading_elm_1)
