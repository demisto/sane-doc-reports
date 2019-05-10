from sane_doc_reports.MarkdownSection import markdown_to_html


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


# def test_markdown_to_html_ul():
#     md_input = '1. test'
#     ex_output = '<ol>\n<li>test</li>\n</ol>'
#     assert markdown_to_html(md_input) == ex_output
#
#
# def test_markdown_to_html_ol():
#     md_input = '- test\n* test2'
#     ex_output = '<ul>\n<li>test</li>\n<li>test2</li>\n</ul>'
#     assert markdown_to_html(md_input) == ex_output
#
#     md_input = '- test\n* test2\n\t- test3'
#     ex_output = '<ul>\n<li>test</li>\n<li>test2<ul>\n<li>test3</li>\n' + \
#                 '</ul>\n</li>\n</ul>'
#     assert markdown_to_html(md_input) == ex_output
#
#
# def test_markdown_to_html_text_styles():
#     md_input = '**test**'
#     ex_output = '<p><strong>test</strong></p>'
#     assert markdown_to_html(md_input) == ex_output
#
#     md_input = '~~test~~'
#     ex_output = '<p><del>test</del></p>'
#     assert markdown_to_html(md_input) == ex_output
#
#     md_input = '*test*'
#     ex_output = '<p><em>test</em></p>'
#     assert markdown_to_html(md_input) == ex_output
#
#     md_input = '- *test*'
#     ex_output = '<ul>\n<li><em>test</em></li>\n</ul>'
#     assert markdown_to_html(md_input) == ex_output
#
#
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
#
#
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
