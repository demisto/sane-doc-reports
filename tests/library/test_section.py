from sane_doc_reports.conf import ROW_POSITION_KEY, COL_POSITION_KEY, \
    HEIGHT_POSITION_KEY, WIDTH_POSITION_KEY
from tests.utils import get_mock

from sane_doc_reports.Section import sane_to_section, Section


def test_sane_to_section_text():
    json = get_mock('docx/text.json', ret_dict=True)

    s = sane_to_section(json[0])
    assert isinstance(s, Section)
    assert s.type == 'text'
    assert isinstance(s.contents, str)
    assert all([i in s.layout for i in
                [ROW_POSITION_KEY, COL_POSITION_KEY, HEIGHT_POSITION_KEY,
                 WIDTH_POSITION_KEY]])


def test_sane_to_section_markdown():
    json = get_mock('docx/markdown.json', ret_dict=True)

    s = sane_to_section(json[0])
    assert isinstance(s, Section)
    assert s.type == 'markdown'
    assert isinstance(s.contents, str)
    assert all([i in s.layout for i in
                [ROW_POSITION_KEY, COL_POSITION_KEY, HEIGHT_POSITION_KEY,
                 WIDTH_POSITION_KEY]])


def test_sane_to_section_image():
    json = get_mock('docx/image.json', ret_dict=True)

    s = sane_to_section(json[0])
    assert isinstance(s, Section)
    assert s.type == 'image'
    assert isinstance(s.contents, str)
    assert all([i in s.layout for i in
                [ROW_POSITION_KEY, COL_POSITION_KEY, HEIGHT_POSITION_KEY,
                 WIDTH_POSITION_KEY]])


def test_sane_to_section_table():
    json = get_mock('docx/table.json', ret_dict=True)

    s = sane_to_section(json[0])
    assert isinstance(s, Section)
    assert s.type == 'table'
    assert isinstance(s.contents, list)
    assert isinstance(s.contents[0], dict)
    assert all([i in s.layout for i in
                [ROW_POSITION_KEY, COL_POSITION_KEY, HEIGHT_POSITION_KEY,
                 WIDTH_POSITION_KEY]])


def test_sane_to_section_quote():
    # TODO: make sure that quote contents has a list
    json = get_mock('docx/quote.json', ret_dict=True)

    s = sane_to_section(json[0])
    assert isinstance(s, Section)
    assert s.type == 'markdown'
    assert isinstance(s.contents, str)
    assert isinstance(s.contents[0], dict)
    assert all([i in s.layout for i in
                [ROW_POSITION_KEY, COL_POSITION_KEY, HEIGHT_POSITION_KEY,
                 WIDTH_POSITION_KEY]])


def test_sane_to_section_number_trend():
    json = get_mock('docx/number_and_trend.json', ret_dict=True)

    s = sane_to_section(json[0])
    assert isinstance(s, Section)
    assert s.type == 'number'
    assert isinstance(s.contents, int)
    assert all([i in s.layout for i in
                [ROW_POSITION_KEY, COL_POSITION_KEY, HEIGHT_POSITION_KEY,
                 WIDTH_POSITION_KEY]])

    s = sane_to_section(json[1])
    assert isinstance(s, Section)
    assert s.type == 'trend'
    assert isinstance(s.contents, dict)
    assert all([i in s.layout for i in
                [ROW_POSITION_KEY, COL_POSITION_KEY, HEIGHT_POSITION_KEY,
                 WIDTH_POSITION_KEY]])
