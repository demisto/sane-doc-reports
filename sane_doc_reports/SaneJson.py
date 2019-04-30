import json
from typing import Any, Callable, Dict, List, Optional, Type, Union, Tuple

from sane_doc_reports.json_schema import validate
from sane_doc_reports.positioning import *
from sane_doc_reports.Page import Page


def _is_page_separator(json_section: dict):
    if LAYOUT_KEY not in json_section:
        return False
    if STYLE_KEY not in json_section[LAYOUT_KEY]:
        return False
    if PAGEBREAK_KEY not in json_section[LAYOUT_KEY][STYLE_KEY]:
        return False

    return json_section[LAYOUT_KEY][STYLE_KEY][PAGEBREAK_KEY] == "always"


class SaneJson:
    def __init__(self, json_file_path: str) -> None:
        self.file_path = json_file_path
        with open(json_file_path, 'r') as f:
            self.json_data = json.load(f)

        self._verify_sane_json()
        self.pages = self._separate_pages()

    def _verify_sane_json(self):
        return validate(self.json_data)

    def _separate_pages(self) -> List[List[Page]]:
        """
        A page is a list of dicts (each dict is an section in the page), sections in
        the page are sorted by the ROW_POSITION_KEY.
        """

        # Let's sort the report by from the top downwards (by ROW_POSITION_KEY)
        report_json_sorted = sorted(self.json_data,
                                    key=lambda k: row_pos(k))

        # Let's split by any page break
        pages = []
        current_page = Page()

        # Split the sections into pages
        for index, json_section in enumerate(report_json_sorted):

            # Check if we hit a page break
            # (add to current page and start a new one)
            if _is_page_separator(json_section):
                pages.append(current_page)
                current_page = Page()

            current_page.add_section(json_section)

            # Check if we get the end of the sections
            if index == len(report_json_sorted) - 1:
                pages.append(current_page)
                continue

        # Normalize all of the vertical positions
        # and fix order for merge, see @merge_cells
        for page in pages:
            page.normalize_row_positions()

        return pages

    def get_page(self, page_index: int) -> Page:
        return self.pages[page_index]

    def get_pages(self) -> Page:
        for page in self.pages:
            yield page
