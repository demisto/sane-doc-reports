from docx.shared import Pt

from sane_doc_reports.domain.CellObject import CellObject
from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG, TREND_MAIN_NUMBER_FONT_SIZE, \
    ALIGN_RIGHT, TREND_SECOND_NUMBER_FONT_SIZE
from sane_doc_reports.elements import error


class TrendElement(Element):

    def insert(self):
        if DEBUG:
            print("Adding trend...")

        table = self.cell_object.cell.add_table(rows=2, cols=4)

        # Add the main number
        current_sum = self.section.contents['currSum']
        inner_cell = table.cell(0, 1)
        main_number = CellObject(inner_cell)
        main_number.run.text = str(current_sum)
        main_number.run.font.size = Pt(TREND_MAIN_NUMBER_FONT_SIZE)
        main_number.run.font.bold = True
        main_number.paragraph.alignment = ALIGN_RIGHT

        # Add the trend number
        previous_sum = self.section.contents['prevSum']
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
        trend_number = CellObject(inner_cell)
        trend_number.run.text = value_percent
        trend_number.run.font.size = Pt(TREND_SECOND_NUMBER_FONT_SIZE)
        trend_number.run.font.bold = False
        trend_number.paragraph.alignment = ALIGN_RIGHT

        # Add the title
        third_cell = table.cell(1, 1)
        table.cell(1, 2).merge(third_cell)
        title = CellObject(third_cell)
        title.run.text = str(self.section.extra['title'])
        title.run.font.size = Pt(TREND_SECOND_NUMBER_FONT_SIZE)
        title.run.font.bold = False
        title.paragraph.alignment = ALIGN_RIGHT


def invoke(cell_object, section):
    if section.type != 'trend':
        section.contents = f'Called trend but not trend -  [{section}]'
        return error.invoke(cell_object,  section)

    TrendElement(cell_object, section).insert()
