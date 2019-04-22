from typing import Dict

from sane_doc_reports import utils
from sane_doc_reports.conf import DEBUG, DATA_KEY

import matplotlib.pyplot as plt

from sane_doc_reports.docx import image


@utils.plot
def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am bar chart!")

    bar_width = 0.35

    data = section[f'{DATA_KEY}']
    objects = [i['name'] for i in data]

    y_axis = [i for i, _ in enumerate(objects)]
    x_axis = [i['data'][0] for i in data]

    # Colors:
    colors = [c for c in utils.get_saturated_colors()[:len(objects)]]

    rects = plt.barh(y_axis, x_axis, align='center', alpha=0.5, color=colors)

    ax = plt.gca()
    ax.set_yticks(y_axis)
    ax.set_yticklabels([])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('')

    ax.set_xlim(-len(objects), len(objects))

    # Remove the bottom labels
    plt.tick_params(bottom='off')
    plt.title(section['title'])

    ax.legend((rects), (objects))

    plt_b64 = utils.plt_t0_b64(plt)
    s = {
        'type': 'image',
        'data': plt_b64
    }
    image.insert(cell_object, s)
