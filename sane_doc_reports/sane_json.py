import json
from typing import Any, Callable, Dict, List, Optional, Type, Union, Tuple

from sane_doc_reports.positioning import *
from sane_doc_reports.page import Page


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
        if not isinstance(self.json_data, list):
            raise ValueError('report json is not a list')

        for section in self.json_data:
            if LAYOUT_KEY not in section:
                raise ValueError(
                    f'report has one or more sections without a {LAYOUT_KEY}')

            # Check that we have all of the layout required keys
            # (defined in consts)
            required_keys = [ROW_POSITION_KEY, COL_POSITION_KEY,
                             HEIGHT_POSITION_KEY, WIDTH_POSITION_KEY]
            key_doesnt_exist = [i for i in required_keys if
                                i not in section[LAYOUT_KEY]]
            if len(key_doesnt_exist) > 0:
                raise ValueError(
                    'report has one or more sections without a' +
                    f' {LAYOUT_KEY}>{",".join(key_doesnt_exist)}')

            # Check that each key for width/height is reasonable
            for key in [HEIGHT_POSITION_KEY, WIDTH_POSITION_KEY]:
                if int(section[LAYOUT_KEY][key]) <= 0:
                    raise ValueError(
                        'report has a section with a bad value' +
                        f' layout key {LAYOUT_KEY}>{key}')

            # Check that each key for rowPos/columnPos is reasonable
            for key in [ROW_POSITION_KEY, COL_POSITION_KEY]:
                if int(section[LAYOUT_KEY][key]) < 0:
                    raise ValueError(
                        'report has a section with a bad value' +
                        f' layout key {LAYOUT_KEY}>{key}')
        return True

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
        should_break_page = False

        # Split the sections into pages
        for index, json_section in enumerate(report_json_sorted):

            # Check if we hit a page break
            # (add to current page and start a new one)
            if _is_page_separator(json_section):
                pages.append(current_page)
                current_page = Page()

            current_page.add_section(json_section)

            # Check if we git the end of the sections
            if index == len(report_json_sorted) - 1:
                pages.append(current_page)
                continue

        # Normalize all of the vertical positions
        # and fix order for merge, see @merge_cells
        for page in pages:
            if isinstance(page, Page):
                page.normalize_row_positions()

        return pages

    def get_page(self, page_index: int) -> Page:
        return self.pages[page_index]

    def get_pages(self) -> Page:
        for page in self.pages:
            yield page
