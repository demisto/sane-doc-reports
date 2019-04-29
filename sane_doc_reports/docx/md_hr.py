from typing import Dict
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn


from sane_doc_reports.conf import DEBUG, DATA_KEY


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am markdown generated horizontal line!")

    p = cell_object['paragraph']._p  # p is the <w:p> XML element
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
