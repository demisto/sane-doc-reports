from pyquery import PyQuery

from sane_doc_reports.MarkdownConverter import markdown_to_html, \
    fix_unwrapped_text


def pq_to_html(pq_object: PyQuery) -> str:
    return str(pq_object).replace('<hr/>', '<hr>').replace('<div>', '').replace(
        '</div>', '')


def test_markdown_to_html_default():
    md_input = 'test'
    ex_output = '<p>test</p>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_header():
    md_input = '### test'
    ex_output = '<h3>test</h3>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_paragraph():
    md_input = 'test\n\ntest'
    ex_output = '<p>test</p>\n<p>test</p>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_link():
    md_input = '[text](url)'
    ex_output = '<p><a href="url">text</a></p>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_code():
    md_input = 'test'
    ex_output = '<p>test</p>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_quote():
    md_input = '> test'
    ex_output = '<blockquote><p>test</p>\n</blockquote>'  # ***
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_hr():
    md_input = '\n---\n'
    ex_output = '<hr>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_ul():
    md_input = '1. test'
    ex_output = '<ol>\n<li>test</li>\n</ol>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_ol():
    md_input = '- test\n* test2'
    ex_output = '<ul>\n<li>test</li>\n<li>test2</li>\n</ul>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output

    md_input = '- test\n* test2\n\t- test3'
    ex_output = '<ul>\n<li>test</li>\n<li>test2<ul>\n<li>test3</li>\n' + \
                '</ul>\n</li>\n</ul>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_markdown_to_html_text_styles():
    md_input = '**test**'
    ex_output = '<p><strong>test</strong></p>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output

    md_input = '~~test~~'
    ex_output = '<p><del>test</del></p>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output

    md_input = '*test*'
    ex_output = '<p><em>test</em></p>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output

    md_input = '- *test*'
    ex_output = '<ul>\n<li><em>test</em></li>\n</ul>'
    assert pq_to_html(markdown_to_html(md_input)) == ex_output


def test_fix_unwrapped_text_stop_condition():
    md_input = 'unwrapped'
    ex_output = '<span>unwrapped</span>'
    assert fix_unwrapped_text(md_input) == ex_output


def test_fix_unwrapped_text_basic():
    md_input = '<p><strong>test</strong> unwrapped</p>'
    ex_output = '<p><span><strong>test</strong></span><span> unwrapped' + \
                '</span></p>'
    assert fix_unwrapped_text(md_input) == ex_output


def test_html_to_section():
    pass
