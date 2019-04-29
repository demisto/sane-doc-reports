from sane_doc_reports.utils import markdown_to_list


def test_markdown_to_list():
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


def test_markdown_to_list_ul():
    markdown = '- **~~123~~**\n- 321'
    md_list = markdown_to_list(markdown)

    expected = [
        {
            'type': 'ul',
            'attrs': [],
            'contents': [
                {
                    'type': 'li',
                    'attrs': ['bold', 'strikethrough'],
                    'contents': '123'

                },
                {
                    'type': 'li',
                    'attrs': [],
                    'contents': '321'
                }
            ]}
    ]
    assert md_list == expected


def test_markdown_to_list_ul_header():
    markdown = '- **~~123~~456**\n- 321\n\n# Header  '
    md_list = markdown_to_list(markdown)

    expected = [
        {
            'type': 'ul',
            'attrs': [],
            'contents': [
                {
                    'type': 'li',
                    'attrs': ['bold', 'strikethrough'],
                    'contents': '123'

                },
                {
                    'type': 'li',
                    'attrs': [],
                    'contents': '321'
                }
            ]
        },
        {'attrs': [], 'contents': 'Header', 'type': 'h1'}
    ]
    assert md_list == expected


def test_markdown_to_list_complex():
    markdown = '''- **a**
- _b_
1. ~~c~~
2. ```print('hi')```
3. [url](url)
4. > Some Quote

~~**# _test_**~~
---'''
    md_list = markdown_to_list(markdown)
    expected = [
        {
            'type': 'ul',
            'attrs': [],
            'contents': [
                {
                    'type': 'li',
                    'attrs': ['bold'],
                    'contents': 'a'

                },
                {
                    'type': 'li',
                    'attrs': ['italic'],
                    'contents': 'b'
                }
            ]
        },
        {
            'type': 'ol',
            'attrs': [],
            'contents': [
                {
                    'type': 'li',
                    'attrs': ['strikethrough'],
                    'contents': 'c'

                },
                {
                    'type': 'li',
                    'attrs': [],
                    'contents': [{
                        'type': 'code',
                        'attrs': [],
                        'contents': "print('hi')"

                    }]
                },
                {
                    'type': 'li',
                    'attrs': [],
                    'contents': [{
                        'type': 'a',
                        'attrs': [],
                        'contents': 'url'
                    }]
                },
                {
                    'type': 'li',
                    'attrs': [],
                    'contents': [
                        {
                            'type': 'blockquote',
                            'attrs': [],
                            'contents': [{
                                'type': 'p',
                                'attrs': [],
                                'contents': 'Some Quote'
                            }]
                        }
                    ]
                },
            ]
        },
        {'attrs': ['bold', 'italic', 'strikethrough'], 'contents': 'test', 'type': 'h2'}
    ]
    assert md_list == expected

