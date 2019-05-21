from typing import List

from sane_doc_reports.domain.Page import Page
from sane_doc_reports.domain.SaneJson import SaneJson


class Transform:
    """ Transforming the sane json into sections per page """

    def __init__(self, sane_json: SaneJson):
        self.sane_json = sane_json

    def get_pages(self) -> List[Page]:
        """
        Get pages and their corresponding section/wrapper objects.
        """
        pages = []

        for _, sane_page in enumerate(self.sane_json.get_sane_pages()):
            page = Page(sane_page)
            page.transform()
            pages.append(page)

        return pages
