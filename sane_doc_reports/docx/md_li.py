from sane_doc_reports import utils
from sane_doc_reports.MarkdownSection import MarkdownSection
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.docx import markdown, error
from sane_doc_reports.utils import get_current_li


class LiWrapper(Wrapper):

    def wrap(self):
        if DEBUG:
            print("Wrapping list item...")

        p_style, list_level, list_type = get_current_li(self.section.extra,
                                                        'List Number')
        self.cell_object.add_paragraph(style=p_style)
        utils.list_number(self.cell_object.cell, self.cell_object.paragraph,
                          level=list_level, num=True)

        if isinstance(self.section.contents, str):
            self.cell_object.run.add_text(self.section.contents)
            return

        temp_section = MarkdownSection('markdown', self.section.contents, {},
                                       {})
        markdown.invoke(self.cell_object, temp_section,
                        invoked_from_wrapper=True)


def invoke(cell_object, section):
    if section.type != 'li':
        section.contents = f'Called li but not li -  [{section}]'
        return error.invoke(cell_object, section)

    LiWrapper(cell_object, section).wrap()