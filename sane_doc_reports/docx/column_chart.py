from typing import Dict

from sane_doc_reports import utils
from sane_doc_reports.conf import DEBUG, DATA_KEY, DEFAULT_BAR_WIDTH, \
    DEFAULT_ALPHA, LAYOUT_KEY, DEFAULT_BAR_ALPHA

import matplotlib.pyplot as plt

from sane_doc_reports.docx import image
from sane_doc_reports.utils import get_ax_location, get_colors


@utils.plot
def insert(cell_object: Dict, section: Dict) -> None:
    """
    This is a standing barchart (bar goes up)
    """
    if DEBUG:
        print("Yo I am column chart!")

    # Fix sizing
    size_w, size_h, dpi = utils.convert_plt_size(section)
    plt.figure(figsize=(size_w, size_h), dpi=dpi)

    data = section.get(DATA_KEY, [])
    objects = [i['name'] for i in data]

    y_axis = [i for i in range(len(objects))]
    x_axis = [i['data'][0] for i in data]

    colors = get_colors(section[LAYOUT_KEY], objects)

    rects = plt.bar(y_axis, x_axis, align='center', alpha=DEFAULT_BAR_ALPHA,
                    width=DEFAULT_BAR_WIDTH, color=colors)

    ax = plt.gca()

    # Fix the legend values to be "some_value (some_number)" instead of
    # just "some_value"
    fixed_legends = [f'{v} ({x_axis[i]})' for i, v in enumerate(objects)]

    legend_style = section[LAYOUT_KEY]['legendStyle']
    ax.legend(rects, fixed_legends,
              loc=get_ax_location(legend_style)).get_frame().set_alpha(
        DEFAULT_ALPHA)
    ax.set_xlim(-len(objects), len(objects))

    plt.xticks(y_axis, objects)
    plt.title(section['title'])

    plt_b64 = utils.plt_t0_b64(plt)
    s = {
        'type': 'image',
        'data': plt_b64
    }
    image.insert(cell_object, s)
