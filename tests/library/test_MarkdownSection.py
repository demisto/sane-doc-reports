from pyquery import PyQuery

from sane_doc_reports.MarkdownSection import _build_dict, \
    markdown_to_section_list, MarkdownSection
from sane_doc_reports.md_html_fixer import markdown_to_html, fix_unwrapped_text


def test_build_dict_basic():
    markdown_string = 'some string'  # 'tes *can **also*** be ~~the~~ nested...'
    html = fix_unwrapped_text(markdown_to_html(markdown_string), alread)
    root_elem = PyQuery(html)
    res = _build_dict(root_elem)
    expected = {'type': 'p', 'contents': 'some string', 'attrs': [],
                'layout': {}, 'extra': {}}
    assert res == expected


def test_build_dict_basic_element():
    markdown_string = 'some **string**'
    html = markdown_to_html(markdown_string)
    root_elem = PyQuery(html)
    res = _build_dict(root_elem)
    expected = {'type': 'p', 'contents': [
        {'type': 'span', 'contents': 'some ', 'attrs': [],
         'layout': {}, 'extra': {}},
        {'type': 'span', 'contents': [
            {'type': 'strong', 'contents': 'string', 'attrs': [],
             'layout': {}, 'extra': {}}
        ], 'attrs': [], 'layout': {}, 'extra': {}}
    ], 'attrs': [], 'layout': {}, 'extra': {}
                }
    assert res == expected


def test_build_dict_basic_element_attribute():
    markdown_string = 'some [string](url)'
    html = markdown_to_html(markdown_string)
    root_elem = PyQuery(html)
    res = _build_dict(root_elem)
    expected = {'type': 'p', 'contents': [
        {'type': 'span', 'contents': 'some ', 'attrs': [],
         'layout': {}, 'extra': {}},
        {'type': 'span', 'contents': [
            {'type': 'a', 'contents': 'string', 'attrs': [], 'layout': {},
             'extra': {'href': 'url'}}]
            , 'attrs': [], 'layout': {}, 'extra': {}}
    ], 'attrs': [], 'layout': {}, 'extra': {}
                }
    assert res == expected


def test_build_dict_text_and_elements():
    markdown_string = 'some **string** and more strings'
    html = markdown_to_html(markdown_string)
    root_elem = PyQuery(html)
    res = _build_dict(root_elem)
    expected = {'type': 'p', 'contents': [

        {'type': 'span', 'contents': 'some ', 'attrs': [],
         'layout': {}, 'extra': {}},
        {'type': 'span', 'contents': [
            {'type': 'strong', 'contents': 'string', 'attrs': [],
             'layout': {}, 'extra': {}},
        ], 'attrs': [], 'layout': {}, 'extra': {}},
        {'type': 'span', 'contents': ' and more strings', 'attrs': [],
         'layout': {}, 'extra': {}},

    ], 'attrs': [], 'layout': {}, 'extra': {}
                }
    assert res == expected


def test_markdown_to_section_basic():
    markdown = '~~123~~'
    md_list = markdown_to_section_list(markdown)
    res = [i.get_dict() for i in md_list]
    expected = [{
        'type': 'p',
        'contents': [
            {
                'type': 'span',
                'attrs': ['strikethrough'],
                'extra': {},
                'contents': '123',
                'layout': {}
            }
        ], 'attrs': [], 'extra': {}, 'layout': {}
    }]
    assert res == expected


def test_markdown_to_section_wrapped():
    markdown = '**~~123~~**'
    md_list = markdown_to_section_list(markdown)

    res = [i.get_dict() for i in md_list]
    expected = [{
        'type': 'p',
        'contents': [
            {
                'type': 'span',
                'attrs': ['bold', 'strikethrough'],
                'extra': {},
                'contents': '123',
                'layout': {}
            }
        ], 'attrs': [], 'extra': {}, 'layout': {}
    }]
    assert res == expected


def test_markdown_to_section_list_quote():
    markdown_string = "> Blockquotes *can also* be ~~the~~ nested..."

    s = markdown_to_section_list(markdown_string)

    assert isinstance(s, list)
    assert isinstance(s[0], MarkdownSection)
    assert isinstance(s[0].contents, list)

    # print('*', str(s[0]))
    # assert False
    # assert isinstance(s[0].contents[0], MarkdownSection)
