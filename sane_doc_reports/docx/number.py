from docx.shared import Pt

from sane_doc_reports.CellObject import CellObject
from sane_doc_reports.Element import Element


class NumberElement(Element):

    def insert(self):
        print("Adding number: ", self.section.contents)
        table = self.cell_object.cell.add_table(rows=1, cols=1)

        # Used for debugging:
        # table.style = 'Table Grid'

        # Add the main number
        inner_cell = table.cell(0, 0)

        main_number = CellObject(inner_cell)
        main_number.run.text = str(self.section.contents)
        main_number.run.font.size = Pt(24)
        main_number.run.font.bold = True
        main_number.paragraph.alignment = 1

        # Add the title
        title_paragraph = inner_cell.add_paragraph()
        title_run = title_paragraph.add_run()
        title_run.text = str(self.section.extra['title'])
        title_run.font.size = Pt(14)
        title_run.font.bold = False
        title_paragraph.alignment = 1


def invoke(cell_object, section):
    if section.type != 'number':
        raise ValueError('Called number but not number - ', section)

    return NumberElement(cell_object, section).insert()
