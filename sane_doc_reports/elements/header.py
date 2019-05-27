from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.elements import error
from sane_doc_reports.populate.utils import insert_header


class HeaderElement(Element):
    """ Mainly used to fix the investigation header element """

    def insert(self):
        if DEBUG:
            print('Adding text...')

        insert_header(self.cell_object, self.section.contents, header='h1')


def invoke(cell_object, section) -> None:
    if section.type != 'header':
        section.contents = f'Called header but not header -  [{section}]'
        return error.invoke(cell_object, section)

    HeaderElement(cell_object, section).insert()
