from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG


class HorizontalLineElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding horizontal line...')

        tc = self.cell_object.cell._tc

        # Remove extra paragraphs:
        p = self.cell_object.paragraph._element
        p.getparent().remove(p)
        p._p = p._element = None
        p = self.cell_object.get_last_paragraph()._element
        p.getparent().remove(p)
        p._p = p._element = None

        w_para = OxmlElement('w:p')
        w_ppr = OxmlElement('w:pPr')
        w_pbdr = OxmlElement('w:pPr')
        w_bottom = OxmlElement('w:bottom')
        w_bottom.set(qn('w:val'), 'single')
        w_bottom.set(qn('w:sz'), '6')
        w_bottom.set(qn('w:space'), '1')
        w_bottom.set(qn('w:color'), 'auto')

        w_pbdr.append(w_bottom)
        w_ppr.append(w_pbdr)
        w_para.append(w_ppr)

        tc.append(w_para)

def invoke(cell_object, section):
    if section.type != 'hr':
        raise ValueError('Called hr but not hr - ', section)

    return HorizontalLineElement(cell_object, section).insert()
