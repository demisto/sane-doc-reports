from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from sane_doc_reports.CellObject import CellObject
from sane_doc_reports.MarkdownSection import MarkdownSection
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.docx import markdown
from sane_doc_reports.utils import name_to_hex


class CodeWrapper(Wrapper):

    def wrap(self):
        print("Wrapping code...")
        if 'inline' not in self.section.extra:
            self.cell_object.add_paragraph()
            # TODO: remove newlines from OXML

        new_cell = self.cell_object.cell.add_table(1, 1).cell(0, 0)
        shading_elm_1 = parse_xml(
            f'<w:shd {{}} w:fill="{name_to_hex("whitesmoke")}"/>'.format(
                nsdecls('w')))
        new_cell._tc.get_or_add_tcPr().append(shading_elm_1)

        self.cell_object = CellObject(new_cell)

        contents = self.section.contents
        if isinstance(contents, str):
            temp_section = MarkdownSection('markdown',
                                           [MarkdownSection('span', contents,
                                                            {}, {})]
                                           , {}, {})
        else:
            temp_section = MarkdownSection('markdown',
                                           contents, {}, {})
        markdown.invoke(self.cell_object, temp_section,
                        invoked_from_wrapper=True)


def invoke(cell_object, section):
    if section.type != 'code':
        raise ValueError('Called code but not code - ', section)

    return CodeWrapper(cell_object, section).wrap()
