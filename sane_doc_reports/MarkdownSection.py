from __future__ import annotations  # Used to fix the __init__ of same type

import json
from io import StringIO
from typing import Union, List

import mistune
from lxml.html import soupparser

from sane_doc_reports.Section import Section
from sane_doc_reports.conf import HTML_ATTRIBUTES, HTML_ATTR_MARKDOWN_MAP, \
    HTML_MAP
from sane_doc_reports.markdown_utils import build_dict, collapse_attrs


def _should_collapse(has_siblings, section_type):
    return not has_siblings and section_type in HTML_ATTRIBUTES


class MarkdownSection(Section):
    def __init__(self, type, contents: Union[List[Section], str],
                 layout, extra):

        super().__init__(type, contents, layout, extra)
        self.type = type
        self.__map_types()
        self.attrs = []

        contents = contents
        if isinstance(contents, list):
            self.contents = markdown_to_section_list(self.contents)
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
            for child in self.contents:
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
            self.add_attr(child.attrs + [child.type])
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
        return self.contents[0]

    def is_leaf(self):
        return isinstance(self.contents, str)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)

    def __str__(self):
        return self.toJSON()


def markdown_to_section_list(markdown_string) -> List[MarkdownSection]:
    """ Convert markdown to HTML->Python list,
        This will be a readable list of dicts containing:
            - Type: type of html element
            - Contents: text content or list of other dicts
            - Attrs (any defined sane_doc_reports.conf.HTML_ATTRIBUTES)

        For example:
        markdown = '**~~123~~**'
        -> <p><strong><strike>123</strike></strong></p>
        ->[
          {
            "type": "p",
            "attrs": ["strong","strike"],
            "contents": "123"
          }
        ]
        -> [Section Object]
    """
    html = mistune.markdown(markdown_string).strip()
    etree_root = soupparser.parse(StringIO(html)).getroot()
    html_list = list(map(build_dict, [c for c in list(etree_root)]))
    return collapse_attrs(html_list)
