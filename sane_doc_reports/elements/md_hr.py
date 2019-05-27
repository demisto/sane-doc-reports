from sane_doc_reports.conf import DEBUG, MD_TYPE_HORIZONTAL_LINE
from sane_doc_reports.domain.Element import Element
from sane_doc_reports.elements import error
from sane_doc_reports.populate.utils import insert_text


class HorizontalLineElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding horizontal line...')

        self.cell_object.add_paragraph(add_run=False)
        insert_text(self.cell_object, '⎯' * 64)


def invoke(cell_object, section):
    if section.type != MD_TYPE_HORIZONTAL_LINE:
        section.contents = f'Called hr but not hr -  [{section}]'
        return error.invoke(cell_object, section)

    HorizontalLineElement(cell_object, section).insert()
