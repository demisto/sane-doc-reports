from sane_doc_reports.domain.Section import sane_to_section
from sane_doc_reports.domain import SaneJsonPage
from sane_doc_reports.transform.markdown.md_helpers import markdown_to_section_list


class Page:
    """ Contains Sections relevant for the page"""

    def __init__(self, sane_page: SaneJsonPage):
        self._sane_page = sane_page
        self.sections = []

    def transform(self):
        for sane_section in self._sane_page.get_sections():
            section = sane_to_section(sane_section)

            if section.type == 'markdown':
                section.contents = markdown_to_section_list(section.contents)

            self.sections.append(section)

    def __iter__(self):
        return iter(self.sections)
