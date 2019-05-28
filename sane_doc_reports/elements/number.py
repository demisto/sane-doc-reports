from sane_doc_reports.domain.CellObject import CellObject
from sane_doc_reports.domain.Element import Element
from sane_doc_reports.elements import error
from sane_doc_reports.populate.utils import insert_text
from sane_doc_reports.conf import DEBUG, TREND_MAIN_NUMBER_FONT_SIZE, \
    TREND_SECOND_NUMBER_FONT_SIZE, PYDOCX_TEXT_ALIGN, \
    PYDOCX_FONT_BOLD, PYDOCX_FONT_SIZE, ALIGN_CENTER


class NumberElement(Element):
    style = {
        'main': {
            PYDOCX_FONT_SIZE: TREND_MAIN_NUMBER_FONT_SIZE,
            PYDOCX_FONT_BOLD: True,
            PYDOCX_TEXT_ALIGN: ALIGN_CENTER
        },
        'title': {
            PYDOCX_FONT_SIZE: TREND_SECOND_NUMBER_FONT_SIZE,
            PYDOCX_FONT_BOLD: False,
            PYDOCX_TEXT_ALIGN: ALIGN_CENTER
        }
    }

    def insert(self):
        if DEBUG:
            print('Adding number...')

        table = self.cell_object.cell.add_table(rows=1, cols=1)

        if DEBUG:
            table.style = 'Table Grid'

        # Add the main number
        inner_cell = table.cell(0, 0)
        main_number = CellObject(inner_cell)

        insert_text(main_number, str(self.section.contents), self.style['main'])

        main_number.add_paragraph(add_run=True)
        insert_text(main_number, str(self.section.extra['title']),
                    self.style['title'])


def invoke(cell_object, section):
    if section.type != 'number':
        section.contents = f'Called number but not number -  [{section}]'
        return error.invoke(cell_object, section)

    NumberElement(cell_object, section).insert()
