from sane_doc_reports.Element import Element


class TextElement(Element):

    def insert(self):
        print('Adding text...')
        print(self.section.contents)
        self.cell_object.run.text = self.section.contents


def invoke(cell_object, section) -> None:
    if section.type not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'paragraph',
                            'span', 'text']:
        raise ValueError('Called text but not text - ', section)

    TextElement(cell_object, section).insert()
