import mistune
from pyquery import PyQuery


def markdown_to_html(markdown_string: str) -> PyQuery:
    html = mistune.markdown(markdown_string).strip()
    return PyQuery(html)


def fix_unwrapped_text(elem: PyQuery) -> PyQuery:
    return elem