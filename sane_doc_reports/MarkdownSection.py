from __future__ import annotations  # Used to fix the __init__ of same type

import json
from typing import Union, List

import mistune
from lxml.etree import _ElementUnicodeResult
from pyquery import PyQuery as pq, PyQuery

from sane_doc_reports.Section import Section
from sane_doc_reports.conf import HTML_ATTRIBUTES, HTML_ATTR_MARKDOWN_MAP, \
    HTML_MAP, HTML_NOT_WRAPABLES


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

    def propagate_extra(self, key, value):
        """ propagate an extra down to all children """
        self.extra[key] = value

        if not isinstance(self.contents, list):
            return

        for child in self.contents:
            child.propagate_extra(key, value)

    def __str__(self):
        return self.toJSON()


def _collapse_attrs(section_list):
    ret = []
    for section in section_list:
        if isinstance(section, Section):
            s = MarkdownSection(section.type, section.contents,
                                section.layout, section.extra)
        else:
            s = MarkdownSection(section['type'], section['contents'],
                                section['layout'], section['extra'])
        s.collapse(False)
        ret.append(s)
    return ret


def _wrap(elem):
    span = pq('<span></span>')
    span.html(elem)
    return span


def get_html(children: List) -> str:
    ret = ""
    for child in children:
        if isinstance(child, str):
            ret += child
        else:
            ret += child.outer_html()

    return ret


def check_wrap(tag, children):
    return tag in HTML_NOT_WRAPABLES and len(children) == 1


def fix_unwrapped_text(root_elem):
    tag = root_elem[0].tag
    children = root_elem.contents()
    should_not_wrap = check_wrap(tag, children)
    fixed_children = _fix_unwrapped_text(children, do_not_wrap=should_not_wrap)
    fixed_element = pq(f'<{tag}></{tag}>')
    fixed_element.html(get_html(fixed_children))
    return fixed_element


def _fix_unwrapped_text(children: PyQuery, do_not_wrap=False) -> List[PyQuery]:
    """ Add spans over all elements and their sub elements except other spans"""
    ret = []
    if do_not_wrap:
        for i in children:
            if isinstance(i, str):
                ret.append(i)
            else:
                for fixed in fix_unwrapped_text(pq(i)):
                    ret.append(pq(fixed))  # pq(i).outer_html())
            return ret

    if len(children) == 1 and isinstance(children[0], str):
        return [children[0]]

    for child in children:
        if isinstance(child, str) and len(children) > 1:
            ret.append(_wrap(child))
            continue

        tag = child.tag
        attribs = "".join([f'{k}="{v}" ' for k, v in child.attrib.items()])
        child = pq(child)
        descendants = _fix_unwrapped_text(child.contents(),
                                          do_not_wrap=tag in HTML_NOT_WRAPABLES)
        descendants_html = ""
        for i in descendants:
            if isinstance(i, str):
                descendants_html += i
            else:
                descendants_html += i.outer_html()

        if tag in ['ul', 'span']:
            child.html(descendants_html)
            ret.append(child)
        else:
            child = pq(f'<{tag} {attribs}>{descendants_html}</{tag}>')
            ret.append(_wrap(child))

    return ret


def _build_dict(elem: PyQuery, already_wrapped=False):
    # Find if has children
    elem = pq(elem)
    children = list(elem.contents())
    has_children = len(elem.children()) > 0

    contents = []
    if has_children:
        # Fix unwrapped children
        if not already_wrapped:
            children = fix_unwrapped_text(elem).contents()
            # children = _fix_unwrapped_text(children, do_not_wrap= \
            #     elem[0].tag in HTML_NOT_WRAPABLES)

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


def markdown_to_html(markdown_string):
    html = mistune.markdown(markdown_string).strip()
    html = html.replace('\n', '')  # TODO: fix
    return html


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
    html = markdown_to_html(markdown_string)
    etree_root = pq(html)
    html_list = list(map(_build_dict, [c for c in list(etree_root)]))
    collapsed = _collapse_attrs(html_list)
    print(",".join([str(i) for i in collapsed]))
    return collapsed
