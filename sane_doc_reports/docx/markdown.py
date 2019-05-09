from docx.shared import Pt

from sane_doc_reports import CellObject
from sane_doc_reports.Section import Section
from sane_doc_reports.MarkdownSection import markdown_to_section_list, \
    MarkdownSection
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.docx import text, md_code, md_ul, md_li, md_blockquote, \
    md_hr, md_ol, md_link

import sane_doc_reports.styles.text as text_style
import sane_doc_reports.styles.header as header_style


class MarkdownWrapper(Wrapper):

    def wrap(self, invoked_from_wrapper=False):

        # Handle called from another wrapper.
        if isinstance(self.section.contents, list):
            md_section_list = self.section.contents
        elif invoked_from_wrapper and \
                isinstance(self.section.contents.contents, str):
            md_section_list = [self.section.contents]
        else:
            md_section_list = markdown_to_section_list(self.section.contents)

        if not isinstance(md_section_list, list):
            raise ValueError('Markdown section does not have valid contents ' +
                             '(must be a list)')

        for section in md_section_list:
            self.cell_object.add_run()
            section_type = section.type
            # === Start wrappers ===
            if section_type == 'div':
                temp_section = MarkdownSection('markdown', section.contents,
                                               {}, {})
                invoke(self.cell_object, temp_section)
                continue

            if section_type == 'code':
                md_code.invoke(self.cell_object, section)
                self.cell_object.paragraph = self.cell_object.get_last_paragraph()
                continue

            if section_type == 'blockquote':
                md_blockquote.invoke(self.cell_object, section)
                self.cell_object.paragraph = self.cell_object.get_last_paragraph()
                continue

            if section_type == 'ul':
                md_ul.invoke(self.cell_object, section)
                self.cell_object.paragraph = self.cell_object.get_last_paragraph()
                continue

            if section_type == 'ol':
                md_ol.invoke(self.cell_object, section)
                self.cell_object.paragraph = self.cell_object.get_last_paragraph()
                continue

            if section_type == 'li':
                md_li.invoke(self.cell_object, section)
                continue

            # === Fix wrapped ===
            if isinstance(section.contents, list):
                if section_type == 'span':
                    section.propagate_extra('inline', True)

                temp_section = MarkdownSection('markdown', section.contents,
                                               {}, {}, section.attrs)
                invoke(self.cell_object, temp_section)
                continue

            # === Elements ===

            # Add a block
            if not invoked_from_wrapper:
                self.cell_object.add_paragraph()  # TODO: make sure this is correct

            if section_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                header_style.apply_style(self.cell_object, section)
                text.invoke(self.cell_object, section)
                continue

            if section_type in ['p', 'span']:
                text_style.apply_style(self.cell_object, section)
                text.invoke(self.cell_object, section)
                continue

            if section_type == 'a':
                md_link.invoke(self.cell_object, section)
                continue

            if section_type == 'hr':
                md_hr.invoke(self.cell_object, section)
                continue

            raise ValueError(f'Section type is not defined: {section_type}')


def invoke(cell_object: CellObject, section: Section,
           invoked_from_wrapper=False):
    if section.type != 'markdown':
        raise ValueError('Called markdown but not markdown - ', section)

    MarkdownWrapper(cell_object, section).wrap(
        invoked_from_wrapper=invoked_from_wrapper)
