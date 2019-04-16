from functools import reduce

import pytest
from sane_doc_reports.sane_json import SaneJson, get_vertical_pos
from tests.utils import get_mock
from sane_doc_reports.conf import *


def test_calculate_page_grid():
    sane_json = SaneJson(get_mock('basic.json'))
    page = sane_json.get_page(0)
    assert page.calculate_page_grid() == (12, 2)


def test_no_second_page_exception():
    sane_json = SaneJson(get_mock('basic.json'))
    with pytest.raises(IndexError):
        sane_json.get_page(1)


def test_calculate_page_grid_empty():
    sane_json = SaneJson(get_mock('grid_checks/onecellgrid.json'))
    page = sane_json.get_page(0)
    assert page.calculate_page_grid() == (1, 1)


def test_calculate_page_grid_full():
    sane_json = SaneJson(get_mock('grid_checks/fullgrid.json'))
    page = sane_json.get_page(0)
    assert page.calculate_page_grid() == (12, 12)


def test_calculate_page_grid_merge():
    sane_json = SaneJson(get_mock('grid_checks/mergegrid.json'))
    page = sane_json.get_page(0)
    assert page.calculate_page_grid() == (12, 9)


def test_normalize_row_positions():
    sane_json = SaneJson(get_mock('three_pages.json'))

    for page in sane_json.get_pages():
        sections = page.get_sections()
        assert reduce(lambda last_vertical_pos, current_section:
                      min(
                          get_vertical_pos(last_vertical_pos),
                          get_vertical_pos(current_section)
                      ), sections)[LAYOUT_KEY][ROW_POSITION_KEY] == 0
