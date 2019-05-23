from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.styles.utils import apply_styling


class ErrorElement(Element):
    """ Used to indicate errors in the elements
    (better for debugging problems in the generation)"""

    def insert(self):
        if DEBUG:
            print('Adding error element: ', self.section.contents)

        style = {
            'bold': True,
            'color': '#ff0013',
            'fontSize': 10,
            'underline': False,
            'strikethrough': False,
            'italic': False
        }
        apply_styling(self.cell_object, style)
        error_message = f'ERROR GENERATING SECTION ({self.section.contents})'
        self.cell_object.run.text = error_message


def invoke(cell_object, section) -> None:
    ErrorElement(cell_object, section).insert()
