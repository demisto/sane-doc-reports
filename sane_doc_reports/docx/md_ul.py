from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from sane_doc_reports.CellObject import CellObject
from sane_doc_reports.MarkdownSection import MarkdownSection
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.docx import markdown
from sane_doc_reports.utils import name_to_hex


class UlWrapper(Wrapper):

    def wrap(self):
        print("Ul code...")
        p = self.cell_object.add_paragraph()
        p.style = 'List Bullet'

        temp_section = MarkdownSection('markdown', self.section.contents, {}, {})
        markdown.invoke(self.cell_object, temp_section,
                        invoked_from_wrapper=True)


def invoke(cell_object, section):
    if section.type != 'ul':
        raise ValueError('Called ul but not ul - ', section)

    return UlWrapper(cell_object, section).wrap()
