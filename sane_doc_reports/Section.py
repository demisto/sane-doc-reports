from sane_doc_reports.conf import LAYOUT_KEY, DATA_KEY


class Section(object):
    """ Object that contains element / set of elements """
    def __init__(self, type, contents, attrs, style, extra):
        self.type = type
        self.contents = contents
        self.attrs = attrs
        self.style = style
        self.extra = extra


def sane_to_section(json):

    if isinstance(json, str):
        # We got a single element
        return json

    if 'text' in json[DATA_KEY]:
        # We got a single element (like markdown)
        return json
    
    type = json['type']
    contents = sane_to_section(json[DATA_KEY])
    style = json[LAYOUT_KEY]
    extra = {'title': json['title']}

    return Section(type, contents, style, extra)
