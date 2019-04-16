import importlib

import docx
from docx import Document
from typing import Any, Callable, Dict, List, Optional, Type, Union, Tuple
from sane_doc_reports.conf import DEBUG, LAYOUT_KEY
from sane_doc_reports.sane_json import SaneJson
from sane_doc_reports.grid import get_cell, merge_cells, get_cell_wrappers
from docx.shared import Pt, Mm


class Report:
    """
    In charge of generating a DOCX report form a SANE report (JSON)
    """

    def __init__(self, json_file_path: str):
        self.document = Document()
        self.sane_json = SaneJson(json_file_path)

    def populate_report(self) -> None:
        self._change_page_size()
        self._decrease_layout_margins()
        for page_num, page in enumerate(self.sane_json.get_pages()):
            cols, rows = page.calculate_page_grid()

            if DEBUG:
                print(f'Creating a layout grid of size ({rows},{cols})' +
                      f' for page: {page_num}')
            grid = self.document.add_table(rows=rows, cols=cols)

            if DEBUG:
                grid.style = 'Table Grid'

            for section in page.get_sections():
                cell = get_cell(grid, section)
                merge_cells(grid, section)
                cell_paragraph, cell_run = get_cell_wrappers(cell)
                cell_object = {
                    'cell': cell,
                    'paragraph': cell_paragraph,
                    'run': cell_run
                }
                self._insert_section(cell_object, section)

    def _insert_section(self, cell_object: dict, section: dict) -> None:
        section_type = section['type']

        # Fix the chart name
        if section_type == 'chart':
            section_type = section[LAYOUT_KEY]['chartType'] + '_chart'

        func = importlib.import_module(f'sane_doc_reports.docx.{section_type}')
        func.insert(cell_object, section)

    def save(self, output_file_path: str):
        self.document.save(output_file_path)

    def _change_page_size(self) -> None:
        """ Will change to A4 """
        sections = self.document.sections
        for section in sections:
            section.page_height = Mm(297)
            section.page_width = Mm(210)

    def _decrease_layout_margins(self) -> None:
        sections = self.document.sections
        for section in sections:
            section.top_margin = Pt(10)
            section.bottom_margin = Pt(10)
            section.left_margin = Pt(25)
            section.right_margin = Pt(15)
