
from pyquery import PyQuery as pq, PyQuery


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


def test_fix_unwrapped_text_basic():
    html = '<p>1<b>2</b>3</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span>1</span><span><b>2</b></span><span>3</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_deep():
    html = '<span><strong>12<b>3</b></strong></span>'
    root_elem = pq(html)

    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span><strong><span>12</span><span><b>3</b></span>' +
                  '</strong></span></p>')
    assert res_check == expected.html()


def test_fix_unwrapped_text_unwrapped():
    html = '<p><i>a</i><b>b</b><c>c</c></p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span><i>a</i></span><span><b>b</b></span><span><c>c' +
                  '</c></span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_no_unwrapped_basic():
    html = '<span><strong>123</strong></span>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span><strong>123</strong></span></p>')
    assert res_check == expected.html()


def test_fix_unwrapped_text_no_unwrapped_basic2():
    html = '<p><span>123</span></p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span>123</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_no_unwrapped_complex():
    html = '<p><span><i>a</i></span><span><b>b</b></span></p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span><i>a</i></span><span><b>b</b></span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic2():
    html = '<p><b>2</b>3</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span><b>2</b></span><span>3</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_basic_3():
    html = '<ul><li>123</li></ul>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<ul><li>123</li></ul>')
    assert res_check == expected.outer_html()


def test_build_dict_ol_with_nesting():
    markdown_string = '1. parent\n2. child\n\t1. nested'
    html = markdown_to_html(markdown_string).strip()
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq(
        '<ol><li>parent</li><li><span>child</span><ol><li>nested</li>' +
        '</ol></li></ol>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex():
    html = '<p>aaa <em>bbb <i>ccc</i></em> ddd <del>eee</del> fff</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i>ccc</i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex2():
    html = '<p>aaa <em>bbb <i>ccc<q>zzz</q>ddd</i></em> ddd <del>eee</del> fff</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
    expected = pq('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><q>zzz</q></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()


def test_fix_unwrapped_text_complex3():
    html = '<p>aaa <em>bbb <i>ccc<span><p>zzz</p></span>ddd</i>' + \
           '</em> ddd <del>eee</del> fff</p>'
    root_elem = pq(html)
    res = fix_unwrapped_text(root_elem)
    res_check = res.outer_html()
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
    res_check = res.outer_html()
    expected = pq('<p><span>aaa </span><span><em><span>bbb </span><span>' +
                  '<i><span>ccc</span><span><p>zzz</p></span><span>ddd' +
                  '</span></i></span></em></span><span> ddd </span><span>' +
                  '<del>eee</del></span><span> fff</span></p>')
    assert res_check == expected.outer_html()
# def test_fix_unwrapped_text_stop_condition_unchanged():
#     html_input = 'unwrapped'
#     ex_output = 'unwrapped'
#     assert fix_unwrapped_text(html_input, already_wrapped=True) == ex_output
#
#
# def test_fix_unwrapped_text_stop_condition():
#     html_input = '<em>unwrapped</em>'
#     ex_output = '<em>unwrapped</em>'
#     assert fix_unwrapped_text(html_input, already_wrapped=True) == ex_output


# def test_fix_unwrapped_text_basic():
#     html_input = 'wrapped'
#     ex_output = '<span>wrapped</span>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_unchanged_basic():
#     html_input = '<span>wrapped</span>'
#     ex_output = '<span>wrapped</span>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_basic_p():
#     html_input = '<p><strong>test</strong> unwrapped</p>'
#     ex_output = '<p><span><strong>test</strong></span><span> unwrapped' + \
#                 '</span></p>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_basic_attrib():
#     html_input = '<p><strong attr="123">test</strong> unwrapped</p>'
#     ex_output = '<p><span><strong attr="123">test</strong></span><span>' + \
#                 ' unwrapped</span></p>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_deep():
#     html_input = '<p><strong><em>test</em> unwrapped</strong></p>'
#     ex_output = '<p><span><strong><span><em>test</em></span><span>' + \
#                 ' unwrapped</span></strong></span></p>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_unchanged_deep():
#     html_input = '<span><span>wrapped</span></span>'
#     ex_output = '<span><span>wrapped</span></span>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_unchanged_deep_other_tags():  # MAY allow inner span
#     html_input = '<span><em>wrapped</em></span>'
#     ex_output = '<span><em>wrapped</em></span>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_complex_deep():
#     html_input = '<p>aaa <em>bbb <i>ccc<q>zzz</q>ddd</i></em> ddd <del>' + \
#                  'eee</del> fff</p>'
#     ex_output = '<p><span>aaa </span><span><em><span>bbb </span>' + \
#                 '<span><i><span>ccc</span><span><q><span>zzz</span></q>' + \
#                 '</span><span>ddd</span></i></span></em></span><span> ddd ' + \
#                 '</span><span><del>eee</del></span><span> fff</span></p>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# def test_fix_unwrapped_text_complex_deep_elements():
#     html_input = '<p>aaa <em>bbb <i>ccc<span><p>zzz</p></span>ddd</i>' + \
#                  '</em> ddd <del>eee</del> fff</p>'
#     ex_output = '<p><span>aaa </span><span><em><span>bbb </span>' + \
#                 '<span><i><span>ccc</span><span><p>zzz</p>' + \
#                 '</span><span>ddd</span></i></span></em></span><span> ddd ' + \
#                 '</span><span><del>eee</del></span><span> fff</span></p>'
#     assert fix_unwrapped_text(html_input) == ex_output
#
#
# # def test_fix_unwrapped_text_unchanged_complex():
# #     html_input = '<p><span>aaa </span><span><em><span>bbb </span>' + \
# #                 '<span><i><span>ccc</span><span><p>zzz</p>' + \
# #                 '</span><span>ddd</span></i></span></em></span><span> ddd ' + \
# #                 '</span><span><del>eee</del></span><span> fff</span></p>'
# #     ex_output = '<p><span>aaa </span><span><em><span>bbb </span>' + \
# #                 '<span><i><span>ccc</span><span><p>zzz</p>' + \
# #                 '</span><span>ddd</span></i></span></em></span><span> ddd ' + \
# #                 '</span><span><del>eee</del></span><span> fff</span></p>'
# #     assert fix_unwrapped_text(html_input) == ex_output
