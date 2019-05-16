from pyquery import PyQuery as PyQuery

from sane_doc_reports.MarkdownSection import markdown_to_html
from sane_doc_reports.md_helpers import fix_unwrapped_text


def test_markdown_to_html_none():
    md_input = None
    ex_output = '<span> </span>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_default():
    md_input = 'test'
    ex_output = '<p>test</p>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_header():
    md_input = '### test'
    ex_output = '<h3>test</h3>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_paragraph():
    md_input = 'test\n\ntest'
    ex_output = '<p>test</p><p>test</p>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_link():
    md_input = '[text](url)'
    ex_output = '<p><a href="url">text</a></p>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_code():
    md_input = 'test'
    ex_output = '<p>test</p>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_quote():
    md_input = '> test'
    ex_output = '<blockquote><p>test</p></blockquote>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_hr():
    md_input = '\n---\n'
    ex_output = '<hr>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_ul():
    md_input = '1. test'
    ex_output = '<ol><li>test</li></ol>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_ol():
    md_input = '- test\n* test2'
    ex_output = '<ul><li>test</li><li>test2</li></ul>'
    assert markdown_to_html(md_input) == ex_output

    md_input = '- test\n* test2\n\t- test3'
    ex_output = '<ul><li>test</li><li>test2<ul><li>test3</li>' + \
                '</ul></li></ul>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_text_styles():
    md_input = '**test**'
    ex_output = '<p><strong>test</strong></p>'
    assert markdown_to_html(md_input) == ex_output

    md_input = '~~test~~'
    ex_output = '<p><del>test</del></p>'
    assert markdown_to_html(md_input) == ex_output

    md_input = '*test*'
    ex_output = '<p><em>test</em></p>'
    assert markdown_to_html(md_input) == ex_output

    md_input = '- *test*'
    ex_output = '<ul><li><em>test</em></li></ul>'
    assert markdown_to_html(md_input) == ex_output


def test_fix_unwrapped_no_tags():
    html = 'test'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p>test</p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_em_tag():
    html = '<em>wrapped</em>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<em>wrapped</em>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic():
    html = '<p>1<b>2</b>3</p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span>1</span><span><b>2</b></span><span>3</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic_2():
    html = '<p><b>2</b>3</p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span><b>2</b></span><span>3</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic_3():
    html = '<p><strong>test</strong> unwrapped</p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span><strong>test</strong></span><span> unwrapped' +
                  '</span<</p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic_4():
    html = '<p><i>a</i><b>b</b><c>c</c></p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span><i>a</i></span><span><b>b</b></span><span><c>c' +
                  '</c></span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_deep():
    html = '<span><strong>12<b>3</b></strong></span>'
    root_elem = PyQuery(html)

    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span><strong><span>12</span><span><b>3</b></span>' +
                  '</strong></span></p>')
    assert res_check == expected.html()


def test_fix_unwrapped_text_attributes():
    html = '<p><strong attr="123">test</strong> unwrapped</p>'
    root_elem = PyQuery(html)

    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span><strong attr="123">test</strong></span>' +
                  '<span> unwrapped</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_no_unwrapped_basic():
    html = '<span>wrapped</span>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<span>wrapped</span>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_no_unwrapped_basic():
    html = '<span><strong>123</strong></span>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span><strong>123</strong></span></p>')
    assert res_check == expected.html()


def test_fix_unwrapped_text_no_unwrapped_basic_2():
    html = '<p><span>123</span></p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span>123</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_no_unwrapped_complex():
    html = '<p><span><i>a</i></span><span><b>b</b></span></p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span><i>a</i></span><span><b>b</b></span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_ul_basic():
    html = '<ul><li>123</li></ul>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<ul><li>123</li></ul>')
    assert res_check == expected.outer_html()


def test_build_dict_ol_with_nesting():
    markdown_string = '1. parent\n2. child\n\t1. nested'
    html = markdown_to_html(markdown_string).strip()
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery(
        '<ol><li>parent</li><li><span>child</span><ol><li>nested</li>' +
        '</ol></li></ol>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex():
    html = '<p>aaa <em>bbb <i>ccc</i></em> ddd <del>eee</del> fff</p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i>ccc</i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex_2():
    html = '<p>aaa <em>bbb <i>ccc<q>zzz</q>ddd</i></em> ddd <del>' + \
           'eee</del> fff</p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><q>zzz</q></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex_3():
    html = '<p>aaa <em>bbb <i>ccc<span><p>zzz</p></span>ddd</i>' + \
           '</em> ddd <del>eee</del> fff</p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><p>zzz</p></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_no_change_fix_unwrapped_text_complex():
    html = '<p><span>aaa </span><span><em><span>bbb </span><span>' + \
           '<i><span>ccc</span><span><p>zzz</p></span><span>ddd' + \
           '</span></i></span></em></span><span> ddd </span><span>' + \
           '<del>eee</del></span><span> fff</span></p>'
    root_elem = PyQuery(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = PyQuery('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><p>zzz</p></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()
