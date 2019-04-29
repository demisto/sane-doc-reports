import json

from sane_doc_reports.conf import HTML_ATTRIBUTES


def should_collapse(has_siblings, section_type):
    return not has_siblings and section_type in HTML_ATTRIBUTES


def collapse_attrs(section_list):
    ret = []
    for section in section_list:
        s = Section(section)
        collapse(s, False)
        ret.append(s.get_dict())
    return ret


def collapse(section, has_siblings):
    """ Recursively collapse the HTML style elements into attributes """

    # If we got to the end return if we should collapse
    if section.is_leaf():
        return should_collapse(has_siblings, section.type)

    # This is the only time when we can collapse
    if section.has_child():
        child = section.get_child()
        collapsible = collapse(child, False)
        if collapsible:
            section.collapse()
        parent_collapsible = should_collapse(has_siblings, child.type)
        if parent_collapsible:
            section.collapse()
        return should_collapse(has_siblings, section.type)

    # Recursively go through all the sections
    if section.has_children():
        for child in section.contents:
            collapsible = collapse(child, True)
            if collapsible:
                child.collapse()

    return False


class Section:
    def __init__(self, section_dict: dict):
        self.type = section_dict['type']
        self.attrs = []

        contents = section_dict['contents']
        if isinstance(contents, list):
            self.contents = list([Section(c) for c in contents])
        else:
            self.contents = contents

    def add_attr(self, attrs):
        new_attributes = set(self.attrs)
        for attr in attrs:
            new_attributes.add(attr)
        self.attrs = sorted(list(new_attributes))

    def collapse(self):
        """ Collapse the child element and move it as an attribute to self """
        if self.has_child():
            child = self.contents[0]
            self.add_attr(child.attrs + [child.type])
            self.contents = child.contents

    def has_children(self):
        return isinstance(self.contents, list) and len(self.contents) > 1

    def has_child(self):
        return isinstance(self.contents, list) and len(self.contents) == 1

    def get_child(self):
        return self.contents[0]

    def is_leaf(self):
        return isinstance(self.contents, str)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)

    def get_dict(self):
        return json.loads(self.toJSON())

    def __str__(self):
        return self.toJSON()


def build_dict(elem):
    children = list(elem)
    has_children = len(children) > 0
    elem_text = elem.text if elem.text else ''

    contents = elem_text.strip()
    if has_children:
        contents = list(map(build_dict, children))

    return {'type': elem.tag, 'attrs': [], 'contents': contents}


