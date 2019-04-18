from typing import Union

from sane_doc_reports.conf import *


def row_pos(section: dict) -> int:
    return section[LAYOUT_KEY][ROW_POSITION_KEY]


def col_pos(section: dict) -> int:
    return section[LAYOUT_KEY][COL_POSITION_KEY]


def get_height(section: dict) -> int:
    """ Get the relative (to the grid) height of the section """
    return section[LAYOUT_KEY][HEIGHT_POSITION_KEY]


def get_width(section: dict) -> int:
    """ Get the relative (to the grid) width of the section """
    return section[LAYOUT_KEY][WIDTH_POSITION_KEY]


def get_vertical_pos(section: Union[dict, int]) -> int:
    """ Returns the element's bottommost position """
    # Because this function is called from reduce, it might send an int
    if isinstance(section, int):
        return section
    return row_pos(section) + get_height(section)


def get_horizontal_pos(section: Union[dict, int]) -> int:
    """ Returns the element's rightmost position """
    # Because this function is called from reduce, it might send an int
    if isinstance(section, int):
        return section
    return col_pos(section) + get_width(section)
