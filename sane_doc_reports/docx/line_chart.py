from sane_doc_reports.Element import Element
from sane_doc_reports.docx import error


class LineChartElement(Element):

    def insert(self):
        print("Adding text...")


def invoke(cell_object, section):
    if section.type != 'line_chart':
        section.contents = f'Called line_chart but not line_chart -  [{section}]'
        return error.invoke(cell_object,  section)

    LineChartElement(cell_object, section).insert()
