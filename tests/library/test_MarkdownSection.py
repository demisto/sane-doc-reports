from io import StringIO

import mistune
from pyquery import PyQuery as pq

from sane_doc_reports.MarkdownSection import markdown_to_section_list, \
    MarkdownSection, _build_dict, _fix_unwrapped_text, fix_unwrapped_text
from sane_doc_reports.conf import HTML_NOT_WRAPABLES


def test_fix_unwrapped_text_basic():
    html = '<p>1<b>2</b>3</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span>1</span><span><b>2</b></span><span>3</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_deep():
    html = '<span><strong>12<b>3</b></strong></span>'
    root_elem = pq(html)

    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span><strong><span>12</span><span><b>3</b></span>' +
                  '</strong></span></p>')
    assert res_check == expected.html()


def test_fix_unwrapped_text_unwrapped():
    html = '<p><i>a</i><b>b</b><c>c</c></p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span><i>a</i></span><span><b>b</b></span><span><c>c' +
                  '</c></span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_no_unwrapped_basic():
    html = '<span><strong>123</strong></span>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span><strong>123</strong></span></p>')
    assert res_check == expected.html()


def test_fix_unwrapped_text_no_unwrapped_basic2():
    html = '<p><span>123</span></p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span>123</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_no_unwrapped_complex():
    html = '<p><span><i>a</i></span><span><b>b</b></span></p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span><i>a</i></span><span><b>b</b></span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic2():
    html = '<p><b>2</b>3</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span><b>2</b></span><span>3</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic_3():
    html = '<ul><li>123</li></ul>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<ul><li>123</li></ul>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex():
    html = '<p>aaa <em>bbb <i>ccc</i></em> ddd <del>eee</del> fff</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i>ccc</i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex2():
    html = '<p>aaa <em>bbb <i>ccc<q>zzz</q>ddd</i></em> ddd <del>eee</del> fff</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><q>zzz</q></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex3():
    html = '<p>aaa <em>bbb <i>ccc<span><p>zzz</p></span>ddd</i></em> ddd <del>eee</del> fff</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><p>zzz</p></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_no_change_fix_unwrapped_text_complex():
    html = '<p><span>aaa </span><span><em><span>bbb </span><span>' + \
           '<i><span>ccc</span><span><p>zzz</p></span><span>ddd' + \
           '</span></i></span></em></span><span> ddd </span><span>' + \
           '<del>eee</del></span><span> fff</span></p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()  # "".join([i.outerHtml() for i in res])
    expected = pq('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><p>zzz</p></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_build_dict_basic():
    markdown_string = 'some string'  # 'tes *can **also*** be ~~the~~ nested...'
    html = mistune.markdown(markdown_string).strip()
    root_elem = pq(html)
    res = _build_dict(root_elem)
    expected = {'type': 'p', 'contents': 'some string', 'attrs': [],
                'layout': {}, 'extra': {}}
    assert res == expected


def test_build_dict_basic_element():
    markdown_string = 'some **string**'
    html = mistune.markdown(markdown_string).strip()
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


def test_build_dict_basic_element_attribute():
    markdown_string = 'some [string](url)'
    html = mistune.markdown(markdown_string).strip()
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
    html = mistune.markdown(markdown_string).strip()
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


def test_markdown_to_section_list_quote():
    markdown_string = "> Blockquotes *can also* be ~~the~~ nested..."

    s = markdown_to_section_list(markdown_string)

    assert isinstance(s, list)
    assert isinstance(s[0], MarkdownSection)
    assert s[0].type == 'blockquote'
    assert isinstance(s[0].contents, list)
    assert isinstance(s[0].contents[0], MarkdownSection)
    assert isinstance(s[0].contents[0].contents[0], MarkdownSection)
    assert s[0].contents[0].contents[0].contents[0].type == 'span'
    assert s[0].contents[0].contents[0].contents[1].type == 'span'
    assert s[0].contents[0].contents[0].contents[2].type == 'span'
    assert s[0].contents[0].contents[0].contents[3].type == 'span'
    assert s[0].contents[0].contents[0].contents[4].type == 'span'