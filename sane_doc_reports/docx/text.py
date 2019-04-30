from sane_doc_reports.Element import Element


class TextElement(Element):

    def insert(self):
        print("Adding text: ", self.section.contents)
        self.cell_object.run.text = self.section.contents


def invoke(cell_object, section) -> None:
    if section.type != 'text':
        raise ValueError('Called text but not text - ', section)

    TextElement(cell_object, section).insert()
