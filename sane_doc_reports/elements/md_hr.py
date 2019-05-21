from sane_doc_reports.domain.Section import Section
from sane_doc_reports.conf import DEBUG, PYDOCX_TEXT_ALIGN, STYLE_KEY, \
    MD_TYPE_HORIZONTAL_LINE
from sane_doc_reports.domain.Element import Element
from sane_doc_reports.elements import error, text


class HorizontalLineElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding horizontal line...')

        # tc = self.cell_object.cell._tc
        # hr_oxml = _create_hr_oxml()
        # tc.append(hr_oxml)

        self.cell_object.add_paragraph(add_run=False)
        section = Section('text', '⎯' * 64, {  # Unicode
            STYLE_KEY: {
                PYDOCX_TEXT_ALIGN: 'center'
            }
        }, {})
        text.invoke(self.cell_object, section)


def invoke(cell_object, section):
    if section.type != MD_TYPE_HORIZONTAL_LINE:
        section.contents = f'Called hr but not hr -  [{section}]'
        return error.invoke(cell_object, section)

    HorizontalLineElement(cell_object, section).insert()