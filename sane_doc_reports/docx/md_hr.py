from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG


class HorizontalLineElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding horizontal line...')

        self.cell_object.add_paragraph()
        self.cell_object.add_paragraph() # TODO: fix this double spacing

        p = self.cell_object.paragraph._p  # p is the <w:p> XML element
        pPr = p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        pPr.insert_element_before(pBdr,
                                  'w:shd', 'w:tabs', 'w:suppressAutoHyphens',
                                  'w:kinsoku', 'w:wordWrap',
                                  'w:overflowPunct', 'w:topLinePunct',
                                  'w:autoSpaceDE', 'w:autoSpaceDN',
                                  'w:bidi', 'w:adjustRightInd', 'w:snapToGrid',
                                  'w:spacing', 'w:ind',
                                  'w:contextualSpacing', 'w:mirrorIndents',
                                  'w:suppressOverlap', 'w:jc',
                                  'w:textDirection', 'w:textAlignment',
                                  'w:textboxTightWrap',
                                  'w:outlineLvl', 'w:divId', 'w:cnfStyle',
                                  'w:rPr', 'w:sectPr',
                                  'w:pPrChange', 'w:p'
                                  )
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), 'auto')
        pBdr.append(bottom)



def invoke(cell_object, section):
    if section.type != 'hr':
        raise ValueError('Called hr but not hr - ', section)

    return HorizontalLineElement(cell_object, section).insert()

# def insert(cell_object: Dict, section: Dict) -> None:
#     if DEBUG:
#         print("Yo I am markdown generated horizontal line!")
#
