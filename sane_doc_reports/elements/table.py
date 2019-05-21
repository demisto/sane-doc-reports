from docx.table import _Cell

from sane_doc_reports.domain.CellObject import CellObject
from sane_doc_reports.domain.Element import Element
from sane_doc_reports.domain.Section import Section
from sane_doc_reports.conf import DEBUG, STYLE_KEY, PYDOCX_FONT_SIZE
from sane_doc_reports.elements import error, text


def insert_text_into_cell(cell: _Cell, text_value: str):
    cell_object = CellObject(cell)
    section = Section('text', text_value, {STYLE_KEY: {PYDOCX_FONT_SIZE: 10}},
                      {})
    text.invoke(cell_object, section)


class TableElement(Element):

    def insert(self):
        if DEBUG:
            print("Adding table...")

        table_data = self.section.contents

        if 'readableHeaders' in self.section.layout:
            table_columns = list(
                self.section.layout['readableHeaders'].values())
        else:
            table_columns = self.section.layout['tableColumns']

        table = self.cell_object.cell.add_table(rows=1, cols=len(table_columns))
        table.style = 'Light Shading'
        hdr_cells = table.rows[0].cells

        for i, header in enumerate(table_columns):
            insert_text_into_cell(hdr_cells[i], header)

        for r in table_data:
            row_cells = table.add_row().cells
            for i, header in enumerate(table_columns):
                if header in r:
                    insert_text_into_cell(row_cells[i], r[header])


def invoke(cell_object, section):
    if section.type != 'table':
        section.contents = f'Called table but not table -  [{section}]'
        return error.invoke(cell_object, section)

    TableElement(cell_object, section).insert()
