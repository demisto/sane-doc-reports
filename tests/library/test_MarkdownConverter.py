from sane_doc_reports.MarkdownConverter import markdown_to_html


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
    ex_output = '<p>test</p>\n<p>test</p>'
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
    ex_output = '<blockquote><p>test</p>\n</blockquote>'  # ***
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_hr():
    md_input = '\n---\n'
    ex_output = '<hr>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_ul():
    md_input = '1. test'
    ex_output = '<ol>\n<li>test</li>\n</ol>'
    assert markdown_to_html(md_input) == ex_output


def test_markdown_to_html_ol():
    md_input = '- test\n* test2'
    ex_output = '<ul>\n<li>test</li>\n<li>test2</li>\n</ul>'
    assert markdown_to_html(md_input) == ex_output

    md_input = '- test\n* test2\n\t- test3'
    ex_output = '<ul>\n<li>test</li>\n<li>test2<ul>\n<li>test3</li>\n' + \
                '</ul>\n</li>\n</ul>'
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
    ex_output = '<ul>\n<li><em>test</em></li>\n</ul>'
    assert markdown_to_html(md_input) == ex_output




def test_fix_unwrapped_text():
    pass


def test_html_to_section():
    pass
