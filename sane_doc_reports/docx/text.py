from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG


class TextElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding text...')

        self.cell_object.run.text = self.section.contents


def invoke(cell_object, section) -> None:
    if section.type not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'paragraph',
                            'span', 'text', 'p']:
        raise ValueError('Called text but not text - ', section)

    TextElement(cell_object, section).insert()
