from __future__ import annotations  # Used to fix the __init__ of same type

import json
from typing import Union, List

from pyquery import PyQuery as PyQuery

from sane_doc_reports.Section import Section
from sane_doc_reports.conf import HTML_ATTRIBUTES, HTML_ATTR_MARKDOWN_MAP, \
    HTML_MAP
from sane_doc_reports.md_html_fixer import fix_unwrapped_text, markdown_to_html


def _should_collapse(has_siblings, section_type):
    return not has_siblings and section_type in HTML_ATTRIBUTES


class MarkdownSection(Section):
    def __init__(self, type, contents: Union[List[Section], str],
                 layout, extra):

        super().__init__(type, contents, layout, extra)
        self.type = type
        self.__map_types()
        self.attrs = []

        if isinstance(contents, list):
            self.contents = _collapse_attrs(contents)
        else:
            self.contents = contents

        self.extra = extra

    def collapse(self, has_siblings) -> bool:
        """ Recursively collapse the HTML style elements into attributes """

        # If we got to the end return if we should collapse
        if self.is_leaf():
            return _should_collapse(has_siblings, self.type)

        # This is the only time when we can collapse
        if self.has_child():
            child = self.get_child()
            collapsible = child.collapse(False)
            if collapsible:
                self.collapse_child()
            parent_collapsible = _should_collapse(has_siblings, child.type)
            if parent_collapsible:
                self.collapse_child()
            return _should_collapse(has_siblings, self.type)

        # Recursively go through all the section.
        if self.has_children():
            for child in self.contents and isinstance(self.contents, list):
                collapsible = child.collapse(True)
                if collapsible:
                    child.collapse_child()
                else:
                    child.swap_attr()
        return False

    def __map_types(self):
        if self.type in HTML_MAP:
            self.type = HTML_MAP[self.type]

    def add_attr(self, attrs):
        new_attributes = set(self.attrs)
        for attr in attrs:
            mapped_attr = attr
            if attr in HTML_ATTR_MARKDOWN_MAP:
                mapped_attr = HTML_ATTR_MARKDOWN_MAP[attr]
            new_attributes.add(mapped_attr)
        self.attrs = sorted(list(new_attributes))

    def collapse_child(self):
        """ Collapse the child element and move it as an attribute to self """
        if self.has_child():
            child = self.contents[0]
            attr_type = [child.type] if child.type in HTML_ATTRIBUTES else []
            self.add_attr(child.attrs + attr_type)
            self.contents = child.contents

    def swap_attr(self):
        """ Swap element type to be textual and move type to be an attr """
        if self.type in HTML_ATTRIBUTES:
            t = self.type
            self.type = 'p'
            self.add_attr([t])

    def has_children(self):
        return isinstance(self.contents, list) and len(self.contents) > 1

    def has_child(self):
        return isinstance(self.contents, list) and len(self.contents) == 1

    def get_child(self) -> MarkdownSection:
        if isinstance(self.contents, list):
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


def _collapse_attrs(section_list):
    ret = []
    for section in section_list:
        s = MarkdownSection(section['type'], section['contents'],
                            section['layout'], section['extra'])
        s.collapse(False)
        ret.append(s)
    return ret


def _build_dict(elem: PyQuery, already_wrapped=False) -> dict:
    # Find if has children
    elem = PyQuery(elem)
    children = list(elem.contents())
    has_children = len(elem.children()) > 0

    contents = []
    if has_children:
        # Fix unwrapped children
        if not already_wrapped:
            children = []
            for child in children:
                child.append(fix_unwrapped_text(PyQuery(child).outer_html()))

        for child in children:
            child_dict = _build_dict(child, already_wrapped=True)
            if child_dict:
                contents.append(child_dict)
    else:
        contents = elem.html()

    extra = {}
    if 'src' in elem[0].attrib:
        extra['src'] = elem.attr('src')
    if 'href' in elem[0].attrib:
        extra['href'] = elem.attr('href')

    return {'type': list(elem)[0].tag, 'attrs': [], 'layout': {},
            'contents': contents,
            'extra': extra}


def markdown_to_section_list(markdown_string) -> List[MarkdownSection]:
    html = markdown_to_html(markdown_string)
    etree_root = PyQuery(html)
    html_list = list(map(_build_dict, [c for c in list(etree_root)]))
    return _collapse_attrs(html_list)