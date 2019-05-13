from typing import Dict

from sane_doc_reports import utils
from sane_doc_reports.conf import DEBUG, DATA_KEY, DEFAULT_ALPHA, \
    DEFAULT_BAR_WIDTH, DEFAULT_BAR_ALPHA, LAYOUT_KEY

import matplotlib.pyplot as plt

from sane_doc_reports.docx import image
from sane_doc_reports.utils import get_colors


@utils.plot
def insert(cell_object: Dict, section: Dict) -> None:
    """
    This is a bar chart on the side (bar goes right)
    """

    if DEBUG:
        print("Yo I am bar chart!")

    # Fix sizing
    size_w, size_h, dpi = utils.convert_plt_size(section)
    plt.figure(figsize=(size_w, size_h), dpi=dpi)

    data = section.get(DATA_KEY, [])
    objects = [i['name'] for i in data]

    y_axis = [i for i in range(len(objects))]
    x_axis = [i['data'][0] for i in data]

    colors = get_colors(section[LAYOUT_KEY], objects)

    rects = plt.barh(y_axis, width=x_axis, align='center',
                     alpha=DEFAULT_BAR_ALPHA,
                     color=colors,
                     height=DEFAULT_BAR_WIDTH)

    # Fix the legend values to be "some_value (some_number)" instead of
    # just "some_value"
    fixed_legends = [f'{v} ({x_axis[i]})' for i, v in enumerate(objects)]

    # Create and move the legend outside
    legend_location = 'upper right'
    legend_location_relative_to_graph = (1.75, 1)

    ax = plt.gca()
    ax.legend(rects, fixed_legends, loc=legend_location,
              bbox_to_anchor=legend_location_relative_to_graph).get_frame() \
        .set_alpha(DEFAULT_ALPHA)

    # Fix the axises
    ax.set_yticks(y_axis)
    ax.set_yticklabels([])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('')

    ax.set_xlim(0, len(objects) + DEFAULT_ALPHA)

    # Remove the bottom labels
    plt.tick_params(bottom='off')
    plt.title(section['title'])

    plt_b64 = utils.plt_t0_b64(plt)
    s = {
        'type': 'image',
        'data': plt_b64
    }
    image.insert(cell_object, s)
