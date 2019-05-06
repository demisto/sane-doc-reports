import mistune


def markdown_to_html(markdown_string):
    html = mistune.markdown(markdown_string).strip()
    return html