from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.elements import error
import sane_doc_reports.styles.text as text_style
from sane_doc_reports.utils import has_run


class TextElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding text...')

        self.cell_object.run.text = self.section.contents


def invoke(cell_object, section, apply_default_styling=True) -> None:
    if section.type not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'paragraph',
                            'span', 'text', 'p']:
        section.contents = f'Called text but not text -  [{section}]'
        return error.invoke(cell_object, section)

    has_run(cell_object)

    if apply_default_styling:
        text_style.apply_style(cell_object, section)

    TextElement(cell_object, section).insert()
