from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.elements import error, md_hr


class HeaderElement(Element):
    """ Mainly used to fix the investigation divider element """

    def insert(self):
        if DEBUG:
            print('Adding text...')

        self.section.type = 'hr'
        md_hr.invoke(self.cell_object, self.section)


def invoke(cell_object, section) -> None:
    if section.type != 'divider':
        section.contents = f'Called divider but not divider -  [{section}]'
        return error.invoke(cell_object, section)

    HeaderElement(cell_object, section).insert()
