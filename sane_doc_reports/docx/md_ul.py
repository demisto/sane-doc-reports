from sane_doc_reports.MarkdownSection import MarkdownSection
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.conf import UNORDERED_LIST_NAME
from sane_doc_reports.docx import markdown
from sane_doc_reports.utils import get_current_li


class UlWrapper(Wrapper):

    def wrap(self):
        print("Ul code...")

        temp_section = MarkdownSection('markdown', self.section.contents, {},
                                       {})
        p_style, list_level, list_type = get_current_li(self.section.extra,
                                                        UNORDERED_LIST_NAME)
        temp_section.propagate_extra('list_level', list_level)
        temp_section.propagate_extra('list_type', list_type)

        markdown.invoke(self.cell_object, temp_section,
                        invoked_from_wrapper=True)


def invoke(cell_object, section):
    if section.type != 'ul':
        raise ValueError('Called ul but not ul - ', section)

    return UlWrapper(cell_object, section).wrap()
