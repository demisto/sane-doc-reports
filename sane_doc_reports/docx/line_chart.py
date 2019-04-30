from sane_doc_reports.Element import Element


class LineChartElement(Element):

    def insert(self):
        print("Adding text: ", self.section.contents)


def invoke(cell_object, section):
    if section.type != 'line_chart':
        raise ValueError('Called line_chart but not line_chart - ', section)

    return LineChartElement(cell_object, section).insert()
