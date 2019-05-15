from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.docx import error


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
            hdr_cells[i].text = header

        for r in table_data:
            row_cells = table.add_row().cells
            for i, header in enumerate(table_columns):
                if header in r:
                    row_cells[i].text = r[header]


def invoke(cell_object, section):
    if section.type != 'table':
        section.contents = f'Called table but not table -  [{section}]'
        return error.invoke(cell_object,  section)

    TableElement(cell_object, section).insert()
