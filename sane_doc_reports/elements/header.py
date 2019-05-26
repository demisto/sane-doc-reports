from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.domain.Section import Section
from sane_doc_reports.elements import error, text
from sane_doc_reports.utils import has_run
import sane_doc_reports.styles.header as header_style


class HeaderElement(Element):
    """ Mainly used to fix the investigation header element """

    def insert(self):
        if DEBUG:
            print('Adding text...')

        section = Section('h1', self.section.contents, {}, {})
        section.layout['HIGHLIGHT'] = True

        has_run(self.cell_object)
        header_style.apply_style(self.cell_object, section)

        text.invoke(self.cell_object, section)


def invoke(cell_object, section) -> None:
    if section.type != 'header':
        section.contents = f'Called header but not header -  [{section}]'
        return error.invoke(cell_object, section)

    HeaderElement(cell_object, section).insert()
