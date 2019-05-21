import json
from typing import List

from sane_doc_reports.domain.Page import Page
from sane_doc_reports.domain.SaneJson import SaneJson


class Transform:
    """ Transforming the sane json into sections per page """

    def __init__(self, sane_json_path: str):
        with open(sane_json_path, 'r') as f:
            self.json_data = json.load(f)

        self.sane_json = SaneJson(self.json_data)

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

    def get_sane_json(self):
        """ Return the transformed sane json """
        return self.sane_json
