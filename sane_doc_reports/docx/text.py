from sane_doc_reports.Element import Element
from sane_doc_reports.docx import error


class TextElement(Element):

    def insert(self):
        print("Adding text: ", self.section.contents)
        self.cell_object.run.text = self.section.contents


def invoke(cell_object, section) -> None:
    if section.type != 'text':
        section.contents = f'Called text but not text -  [{section}]'
        return error.invoke(cell_object,  section)

    TextElement(cell_object, section).insert()
