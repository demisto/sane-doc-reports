from sane_doc_reports.utils import markdown_to_list


def test_markdown_to_list():
    markdown = '**~~123~~**'
    md_list = markdown_to_list(markdown)

    expected = [
        {
            'type': 'p',
            'attrs': ['strike', 'strong'],
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
                    'attrs': ['strike', 'strong'],
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
                    'attrs': ['strike', 'strong'],
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
2. # d 
3. ```print('hi')```
4. [url](url)
5. > Some Quote

~~**# _test_**~~
--- 
test'''
    md_list = markdown_to_list(markdown)
    expected = [
        {
            'type': 'ul',
            'attrs': [],
            'contents': [
                {
                    'type': 'li',
                    'attrs': ['strong'],
                    'contents': 'a'

                },
                {
                    'type': 'li',
                    'attrs': ['em'],
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
                    'attrs': ['strike'],
                    'contents': 'c'

                },
                {
                    'type': 'li',
                    'attrs': [],
                    'contents': [{
                        'type': 'h1',
                        'attrs': [],
                        'contents': 'd'
                    }]
                }
            ]
        }
    ]
    assert md_list == expected


    #TODO: table