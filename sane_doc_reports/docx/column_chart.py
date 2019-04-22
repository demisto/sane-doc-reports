from typing import Dict

from sane_doc_reports import utils
from sane_doc_reports.conf import DEBUG, DATA_KEY

import matplotlib.pyplot as plt

from sane_doc_reports.docx import image


@utils.plot
def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am column chart!")

    bar_width = 0.35

    data = section[f'{DATA_KEY}']
    objects = [i['name'] for i in data]

    y_axis = [i for i, _ in enumerate(objects)]
    x_axis = [i['data'][0] for i in data]

    plt.bar(y_axis, x_axis, align='center', alpha=0.5, width=bar_width)

    ax = plt.gca()
    ax.set_xlim(-len(objects), len(objects))

    plt.xticks(y_axis, objects)
    plt.title(section['title'])

    plt_b64 = utils.plt_t0_b64(plt)
    s = {
        'type': 'image',
        'data': plt_b64
    }
    image.insert(cell_object, s)
