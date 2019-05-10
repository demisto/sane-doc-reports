from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG


class LineChartElement(Element):

    def insert(self):
        if DEBUG:
            print("Adding text...")


def invoke(cell_object, section):
    if section.type != 'line_chart':
        raise ValueError('Called line_chart but not line_chart - ', section)

    return LineChartElement(cell_object, section).insert()
