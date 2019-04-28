from typing import Dict

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt

from sane_doc_reports.conf import DEBUG, DATA_KEY
from sane_doc_reports.grid import get_cell_wrappers


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am a trend!")

    # Used for debugging:
    # table.style = 'Table Grid'
    # wt = cell_object['cell'].add_table(rows=1, cols=1)
    # wt.style = 'Table Grid'
    table = cell_object['cell'].add_table(rows=2, cols=4)

    # Add the main number
    current_sum = section[f'{DATA_KEY}']['currSum']
    inner_cell = table.cell(0, 1)
    inner_cell_paragraph, inner_cell_run = get_cell_wrappers(inner_cell)
    inner_cell_run.text = str(current_sum)
    inner_cell_run.font.size = Pt(24)
    inner_cell_run.font.bold = True
    inner_cell_paragraph.alignment = 1

    # Add the trend number
    previous_sum = section[f'{DATA_KEY}']['prevSum']
    # Fix for the percentages
    if previous_sum == 0:
        previous_sum = 1

    change = (current_sum * 100) / previous_sum
    if change < 0:
        direction = '⏷'  # Down arrow
    else:
        direction = '⏶'  # Up arrow

    value_percent = f'{direction}{change}%'
    inner_cell = table.cell(0, 2)
    inner_cell_paragraph, inner_cell_run = get_cell_wrappers(inner_cell)
    inner_cell_run.text = value_percent
    inner_cell_run.font.size = Pt(14)
    inner_cell_run.font.bold = False
    inner_cell_paragraph.alignment = 1

    # Add the title
    third_cell = table.cell(1, 1)
    table.cell(1, 2).merge(third_cell)
    inner_third_paragraph = third_cell.add_paragraph()
    inner_3rd_run = inner_third_paragraph.add_run()
    inner_3rd_run.text = str(section['title'])
    inner_3rd_run.font.size = Pt(14)
    inner_3rd_run.font.bold = False
    inner_third_paragraph.alignment = 1

    # Add background color
    # TODO: add background color later on.
    # color_str = 'f3f3f3'
    # shading_elm_1 = parse_xml(
    #     (r'<w:shd {} w:fill="' + color_str + '"/>').format(nsdecls('w')))
    # inner_cell._tc.get_or_add_tcPr().append(shading_elm_1)
