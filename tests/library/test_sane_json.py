import pytest
import json

from sane_doc_reports.sane_json import SaneJson
from tests.utils import get_mock
from sane_doc_reports.page import Page


def test_sane_json_constructor():
    sane_json = SaneJson(get_mock('basic.json'))

    assert sane_json
    assert len(sane_json.json_data) == 2
    assert sane_json.json_data[0]['type'] == 'text'
    assert sane_json.json_data[1]['type'] == 'text'


def test_sane_json_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        SaneJson(get_mock('invalid/invalid_json.json'))

    with pytest.raises(json.JSONDecodeError) as e:
        SaneJson(get_mock('invalid/empty.json'))


def test_sane_json_invalid_not_list():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/bad_sane_json_1.json'))
    assert 'report json is not a list' in str(e.value)


def test_sane_json_invalid_no_layout():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/bad_sane_json_2.json'))
    assert 'report has one or more sections without a layout' in str(e.value)


def test_sane_json_invalid_no_col_key():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/bad_sane_json_3.json'))
    assert 'report has one or more sections without a layout>columnPos' in str(
        e.value)


def test_sane_json_invalid_no_row_key():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/bad_sane_json_4.json'))
    assert 'report has one or more sections without a layout>rowPos' in str(
        e.value)


def test_sane_json_invalid_no_width_key():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/bad_sane_json_5.json'))
    assert 'report has one or more sections without a layout>w' in str(
        e.value)


def test_sane_json_invalid_no_height_key():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/bad_sane_json_6.json'))
    assert 'report has one or more sections without a layout>h' in str(
        e.value)


def test_sane_json_invalid_2ndpage_no_height_key():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/bad_sane_json_7.json'))
    assert 'report has one or more sections without a layout>rowPos,h' in str(
        e.value)


def test_sane_json_invalid_not_list():
    with pytest.raises(ValueError) as e:
        SaneJson(get_mock('invalid/invalid_layout_keys.json'))
    assert 'report has a section with a bad value layout key layout>h' in str(
        e.value)


def test__separate_pages():
    # Sorry for checking a private function
    sane_json = SaneJson(get_mock('three_pages.json'))
    assert len(sane_json._separate_pages()) == 3


def test_pages_grid_constructor():
    sane_json = SaneJson(get_mock('basic.json'))
    assert len(sane_json.pages) == 1

    first_page = sane_json.pages[0]
    assert isinstance(first_page, Page)
    assert len(first_page) == 2
