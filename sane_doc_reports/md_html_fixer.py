from typing import Tuple

import mistune
from pyquery import PyQuery
from lxml.etree import tostring, _Element

from sane_doc_reports.conf import HTML_ATTRIBUTES


def markdown_to_html(markdown_string: str) -> str:
    html = mistune.markdown(markdown_string).strip()
    return html


def create_tag(tag_name, html_contents, attribs: dict):
    """ Creates a new PyQyery element with specified tag name and contents """
    attribs = "".join([f'{k}="{v}"" ' for k, v in attribs.items()])
    tag = PyQuery(f'<{tag_name} {attribs}></{tag_name}>')
    tag.html(html_contents)
    return tag


def get_inner_html(elem: PyQuery) -> str:
    ret = ""
    for c in elem.contents():
        if isinstance(c, str):
            ret += c
        else:
            c.tail = ''  # fixes double string bug
            ret += tostring(c).decode("utf-8")
    return ret


def _has_children(elem: PyQuery) -> bool:
    for e in elem.contents():
        if isinstance(e, _Element):
            return True
    return False


def fix_unwrapped_text(elem_str: str, already_wrapped=False) -> str:
    return _fix_unwrapped_text(elem_str, already_wrapped=already_wrapped,
                               first_call=True)


def _fix_unwrapped_text(elem_str: str, already_wrapped=False,
                        first_call=False) -> str:
    elem = PyQuery(elem_str)
    has_children = _has_children(elem)

    # Don't wrap this level, and try to wrap the children if it has them.
    if already_wrapped:
        if has_children:
            ret = []
            for c in elem.contents():
                if isinstance(c, str):
                    ret.append(fix_unwrapped_text(c))
                    continue
                ret.append(_fix_unwrapped_text(PyQuery(c).outer_html()))
            return "".join(ret)
        return elem_str

    # If no children but we need to wrap
    if not has_children:
        if elem[0].tag == 'span':
            return elem_str
        wrapper = create_tag('span', elem_str, {})
        return wrapper.outer_html()

    ret = []
    for child in elem.contents():
        if isinstance(child, str):
            ret.append(_fix_unwrapped_text(child))
            continue

        shouldnot_wrap_inner = child.tag in ['span'] + HTML_ATTRIBUTES
        new_child = create_tag(child.tag, _fix_unwrapped_text(
            get_inner_html(PyQuery(child)),
            already_wrapped=shouldnot_wrap_inner), child.attrib)

        # We didn't wrap the next level but we should wrap this one if it's
        # not a span.
        if child.tag != 'span' and elem[0].tag != 'span':
            ret.append('<span>{}</span>'.format(new_child.outer_html()))
        else:
            ret.append(new_child.outer_html())

    elem.html("".join(ret))
    if not already_wrapped and not first_call:
        return '<span>{}</span>'.format(elem.outer_html())
    return elem.outer_html()
