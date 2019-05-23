import json
from collections import defaultdict
from typing import List

from sane_doc_reports.conf import COL_POSITION_KEY, LAYOUT_KEY, \
    ROW_POSITION_KEY, HEIGHT_POSITION_KEY, WIDTH_POSITION_KEY, DATA_KEY
from sane_doc_reports.domain.Page import Page
from sane_doc_reports.domain.SaneJson import SaneJson


class Transform:
    """ Transforming the sane json into sections per page """

    def __init__(self, sane_json_path: str):
        with open(sane_json_path, 'r') as f:
            self.json_data = json.load(f)

        # Transform the json if it is an investigation json
        if self.is_investigation_json():
            self.json_data = _transform_investigation_json(self.json_data)

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

    def is_investigation_json(self):
        json_data = self.json_data

        # Pass through to the json validation in SaneJson
        if len(json_data) == 0 or not isinstance(json_data, list):
            return False

        # Check basic validity of json, will validate in SaneJson
        if any([LAYOUT_KEY not in i for i in json_data]):
            return

        has_w = WIDTH_POSITION_KEY in json_data[0][LAYOUT_KEY]
        has_h = HEIGHT_POSITION_KEY in json_data[0][LAYOUT_KEY]
        return not has_w or not has_h


def _transform_investigation_json(json_data: List[dict]) -> List[dict]:
    """ Fixes all of the old investigation json format, trying to convert
        it to the new json format.
    """

    # Fix the first element
    json_data[0][LAYOUT_KEY][ROW_POSITION_KEY] = 0
    json_data[0][LAYOUT_KEY][COL_POSITION_KEY] = 0

    # Normalize the rowPos
    json_data.sort(key=lambda item: item[LAYOUT_KEY][ROW_POSITION_KEY])

    # Group for columnPos normalizing (has to be after sorting)
    row_groups = defaultdict(list)
    for i, v in enumerate(json_data):
        row_groups[v[LAYOUT_KEY][ROW_POSITION_KEY]].append(
            {"original_key": i, "section": v})

    # Normalize the columnPos by the groups
    for row in row_groups:
        group = row_groups[row]
        for i, v in enumerate(group):
            section = v['section']
            section[LAYOUT_KEY][COL_POSITION_KEY] = i
            json_data[v['original_key']] = section

    # Remove any 'automation' type (not usable here)
    json_data = [a for a in json_data if a['type'] != 'automation']

    # Fix the rowPos and add height + width
    for i in range(0, len(json_data)):
        # Fix the row position
        json_data[i][LAYOUT_KEY][ROW_POSITION_KEY] = i

        # We need to add widths and heights, old format doesn't have them
        json_data[i][LAYOUT_KEY][HEIGHT_POSITION_KEY] = 1
        json_data[i][LAYOUT_KEY][WIDTH_POSITION_KEY] = 1

        # Fix nil data
        if not json_data[i][DATA_KEY]:
            json_data[i][DATA_KEY] = ""

        if json_data[i]['type'] == 'logo':
            json_data[i]['type'] = 'image'
            continue

        if json_data[i]['type'] == 'globalSection':
            json_data[i]['type'] = 'elem_list'
            json_data[i][DATA_KEY] = _transform_investigation_json(
                json_data[i][DATA_KEY])
            continue

        # Fix the markdown/text/header types
        if json_data[i]['type'] in ['markdown', 'text', 'header']:
            json_data[i][DATA_KEY] = {
                'text': json_data[i][DATA_KEY]}

    return json_data
