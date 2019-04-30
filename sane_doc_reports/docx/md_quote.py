from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from sane_doc_reports.CellObject import CellObject
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.utils import name_to_hex


class QuoteWrapper(Wrapper):

    def wrap(self):
        print("Adding quote: ", self.section.contents)

        quote_cell_objet = CellObject(self.cell_object.cell)
        quote_cell = quote_cell_objet.run.add_table(1, 1).cell(0, 0)
        # Background color
        shading_elm_1 = parse_xml(
            f'<w:shd {{}} w:fill="{name_to_hex("cornsilk")}"/>'.format(
                nsdecls('w')))
        quote_cell.cell._tc.get_or_add_tcPr().append(shading_elm_1)

        # Call the inner elements
        for child in self.section.contents:
            child_markdown =


def invoke(cell_object, section):
    if section.type != 'quote':
        raise ValueError('Called quote but not quote - ', section)

    return QuoteWrapper(cell_object, section).wrap()
