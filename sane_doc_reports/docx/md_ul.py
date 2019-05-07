from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from sane_doc_reports import utils
from sane_doc_reports.CellObject import CellObject
from sane_doc_reports.MarkdownSection import MarkdownSection
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.docx import markdown
from sane_doc_reports.utils import name_to_hex


class UlWrapper(Wrapper):

    def wrap(self):
        print("Ul code...")

        list_level = 1
        p_style = 'List Bullet'
        if 'list_id' in self.section.extra:
            list_level = int(self.section.extra['list_id']) + 1
            p_style = f'List Bullet {list_level}'

        print('ul style:', p_style)
        self.cell_object.add_paragraph(style=p_style)
        utils.list_number(self.cell_object.cell, self.cell_object.paragraph,
                          level=list_level, num=False)

        temp_section = MarkdownSection('markdown', self.section.contents, {},
                                       {})
        temp_section.propagate_extra('list_id', list_level)

        markdown.invoke(self.cell_object, temp_section,
                        invoked_from_wrapper=True)


def invoke(cell_object, section):
    if section.type != 'ul':
        raise ValueError('Called ul but not ul - ', section)

    return UlWrapper(cell_object, section).wrap()
