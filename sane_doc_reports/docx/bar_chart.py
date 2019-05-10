from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG


class BarChartElement(Element):

    def insert(self):
        if DEBUG:
            print("Adding barchart...")


def invoke(cell_object, section):
    if section.type != 'bar_chart':
        raise ValueError('Called bar_chart but not bar_chart - ', section)

    return BarChartElement(cell_object, section).insert()

# def insert(cell_object: Dict, section: Dict) -> None:
#     if DEBUG:
#         print("Yo Im barchart")
