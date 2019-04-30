from sane_doc_reports.Element import Element


class PieChartElement(Element):

    def insert(self):
        print("Adding pie chart: ", self.section.contents)


def invoke(cell_object, section):
    return PieChartElement(cell_object, section).insert()
