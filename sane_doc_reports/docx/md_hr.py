from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from sane_doc_reports.Section import Section
from sane_doc_reports.conf import DEBUG, PYDOCX_TEXT_ALIGN, STYLE_KEY
from sane_doc_reports.Element import Element
from sane_doc_reports.docx import error, text


def _remove_paragraph(p_elem):
    if p_elem is not None and p_elem.getparent() is not None:
        p_elem.getparent().remove(p_elem)
        p_elem._p = p_elem._element = None


def _create_hr_oxml():
    ''' Not working yet '''
    w_para = OxmlElement('w:p')
    w_ppr = OxmlElement('w:pPr')
    w_pbdr = OxmlElement('w:pBdr')

    w_bottom = OxmlElement('w:bottom')
    w_bottom.set(qn('w:val'), 'single')
    w_bottom.set(qn('w:sz'), '6')
    w_bottom.set(qn('w:space'), '1')
    w_bottom.set(qn('w:color'), 'auto')

    w_between = OxmlElement('w:between')
    w_between.set(qn('w:val'), 'single')
    w_between.set(qn('w:sz'), '6')
    w_between.set(qn('w:space'), '1')
    w_between.set(qn('w:color'), 'auto')

    w_pbdr.append(w_bottom)
    w_pbdr.append(w_between)
    w_ppr.append(w_pbdr)
    w_para.append(w_ppr)

    return w_para


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
    if section.type != 'hr':
        section.contents = f'Called hr but not hr -  [{section}]'
        return error.invoke(cell_object, section)

    HorizontalLineElement(cell_object, section).insert()
