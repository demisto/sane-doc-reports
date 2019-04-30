from sane_doc_reports.Section import Section
from sane_doc_reports.markdown_utils import markdown_to_section_list


def test_markdown_to_section_basic():
    return
    markdown = '**~~123~~**'
    md_list = markdown_to_list(markdown)

    expected = [
        {
            'type': 'p',
            'attrs': ['bold', 'strikethrough'],
            'contents': '123'
        }
    ]
    assert md_list == expected


def test_markdown_to_section_list_quote():
    markdown_string = """> Blockquotes *can also* be ~~the~~ nested..."""

    s = markdown_to_section_list(markdown_string)

    assert isinstance(s, Section)
