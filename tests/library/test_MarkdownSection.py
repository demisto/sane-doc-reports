from pyquery import PyQuery as pq

from sane_doc_reports.MarkdownSection import markdown_to_section_list, \
    MarkdownSection, _build_dict, markdown_to_html, _collapse_attrs


def test_build_dict_basic():
    markdown_string = 'some string'  # 'tes *can **also*** be ~~the~~ nested...'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
    res = _build_dict(root_elem)
    expected = {'type': 'p', 'contents': 'some string', 'attrs': [],
                'layout': {}, 'extra': {}}
    assert res == expected


def test_build_dict_basic_element():
    markdown_string = 'some **string**'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
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


def test_build_dict_deep_ul():
    markdown_string = '- parent\n\t- child'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
    res = _build_dict(root_elem)
    expected = {'type': 'ul', 'contents': [
        {'type': 'li', 'attrs': [], 'layout': {}, 'extra': {},  # 0
         'contents': [
             {'type': 'span', 'contents': 'parent', 'attrs': [], 'layout': {},
              'extra': {}},
             {'type': 'ul', 'contents': [
                 {'type': 'li', 'attrs': [], 'layout': {}, 'extra': {},
                  'contents': 'child'}
             ], 'attrs': [], 'layout': {}, 'extra': {}}
         ]
         }], 'attrs': [], 'layout': {}, 'extra': {}
                }
    assert res == expected


def test_build_dict_ol():
    markdown_string = '1. parent\n\t1. child'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
    res = _build_dict(root_elem)
    expected = {'type': 'ol', 'contents': [
        {'type': 'li', 'attrs': [], 'layout': {}, 'extra': {},  # 0
         'contents': [
             {'type': 'span', 'contents': 'parent', 'attrs': [], 'layout': {},
              'extra': {}},
             {'type': 'ol', 'contents': [
                 {'type': 'li', 'attrs': [], 'layout': {}, 'extra': {},
                  'contents': 'child'}
             ], 'attrs': [], 'layout': {}, 'extra': {}}
         ]
         }], 'attrs': [], 'layout': {}, 'extra': {}
                }
    assert res == expected


def test_build_dict_deep_ol():
    markdown_string = '1. parent\n\t1. child\n\t\t1. deep child'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
    res = _build_dict(root_elem)
    expected = {'type': 'ol', 'contents': [
        {'type': 'li', 'attrs': [], 'layout': {}, 'extra': {},  # 0
         'contents': [
             {'type': 'span', 'contents': 'parent', 'attrs': [], 'layout': {},
              'extra': {}},
             {'type': 'ol', 'contents': [
                 {'type': 'li', 'attrs': [], 'layout': {}, 'extra': {},
                  'contents': [
                      {'type': 'span', 'contents': 'child', 'attrs': [],
                       'layout': {},
                       'extra': {}},
                      {'type': 'ol', 'contents': [
                          {'type': 'li', 'contents': 'deep child', 'attrs': [],
                           'layout': {},
                           'extra': {}},
                      ], 'attrs': [],
                       'layout': {},
                       'extra': {}},
                  ]}
             ], 'attrs': [], 'layout': {}, 'extra': {}}
         ]
         }], 'attrs': [], 'layout': {}, 'extra': {}
                }
    assert res == expected


def test_collapse_attrs_ol_deep():
    markdown_string = '1. parent\n\t1. child\n\t\t1. deep child'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
    res = _build_dict(root_elem)
    res = _collapse_attrs([res])

    assert isinstance(res, list)
    assert res[0].type == 'ol'
    assert res[0].contents[0].type == 'li'
    assert res[0].contents[0].contents[1].type == 'ol'
    #       ol      li          ol        li            ol          li
    assert res[0].contents[0].contents[1].contents[0].contents[1].contents[
               0].contents == 'deep child'


def test_build_dict_basic_element_attribute():
    markdown_string = 'some [string](url)'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
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
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
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


def test_markdown_to_section_pre_code():
    markdown = '\n```\ncode\n```\n'
    md_list = markdown_to_section_list(markdown)

    res = [i.get_dict() for i in md_list]
    expected = [{
        'type': 'pre',
        'contents': [
            {
                'type': 'code',
                'attrs': [],
                'extra': {},
                'contents': 'code',
                'layout': {}
            }
        ], 'attrs': [], 'extra': {}, 'layout': {}
    }]
    assert res == expected


def test_markdown_to_section_ul():
    markdown = '- one\n- *two*'
    md_list = markdown_to_section_list(markdown)

    res = [i.get_dict() for i in md_list]
    expected = [{
        'type': 'ul',
        'contents': [
            {'type': 'li', 'attrs': [], 'extra': {}, 'contents': 'one',
             'layout': {}},
            {'type': 'li', 'attrs': ['italic'], 'extra': {}, 'contents': 'two',
             'layout': {}}
        ], 'attrs': [], 'extra': {}, 'layout': {}
    }]
    assert res == expected


def test_markdown_to_section_ul_ol_complex():
    markdown = '- one\n- two\n\t1. nested\n\t2. nested deep'
    md_list = markdown_to_section_list(markdown)

    res = [i.get_dict() for i in md_list]
    expected = [{
        'type': 'ul',
        'contents': [
            {'type': 'li', 'attrs': [], 'extra': {}, 'contents': 'one',
             'layout': {}},
            {'type': 'li', 'attrs': [], 'extra': {}, 'contents': [
                {'type': 'span', 'attrs': [], 'extra': {}, 'contents': 'two',
                 'layout': {}},
                {'type': 'ol', 'attrs': [], 'extra': {}, 'contents': [
                    {'type': 'li', 'attrs': [], 'extra': {},
                     'contents': 'nested',
                     'layout': {}},
                    {'type': 'li', 'attrs': [], 'extra': {},
                     'contents': 'nested deep',
                     'layout': {}}
                ],
                 'layout': {}}
            ],
             'layout': {}},
        ], 'attrs': [], 'extra': {}, 'layout': {}
    }]
    assert res == expected


def test_markdown_to_section_list_quote():
    markdown_string = "> Blockquotes *can also* have ~~the~~ nested..."

    md_list = markdown_to_section_list(markdown_string)

    assert isinstance(md_list, list)
    assert isinstance(md_list[0], MarkdownSection)
    assert md_list[0].type == 'blockquote'

    res = [i.get_dict() for i in md_list]
    expected = [{
        'type': 'blockquote',
        'contents': [
            {
                'type': 'span', 'attrs': [], 'extra': {},
                'contents': 'Blockquotes ', 'layout': {}
            },
            {
                'type': 'span', 'attrs': ['italic'], 'extra': {},
                'contents': 'can also', 'layout': {}
            },
            {
                'type': 'span', 'attrs': [], 'extra': {},
                'contents': ' have ', 'layout': {}
            },
            {
                'type': 'span', 'attrs': ['strikethrough'], 'extra': {},
                'contents': 'the', 'layout': {}
            },
            {
                'type': 'span', 'attrs': [], 'extra': {},
                'contents': ' nested...', 'layout': {}
            }
        ], 'attrs': [], 'extra': {}, 'layout': {}
    }]
    assert res == expected