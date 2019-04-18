import base64
import tempfile
from pathlib import Path
from typing import Dict

from sane_doc_reports.conf import DEBUG, DATA_KEY, LAYOUT_KEY

# Plot
import matplotlib.pyplot as plt

from sane_doc_reports.docx import image


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("I'm a pie chart")

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    data = [int(i['data'][0]) for i in section[DATA_KEY]]
    keys = [i['name'] for i in section[DATA_KEY]]

    def func(percent, total):
        return "{:.1f}%".format(percent, 100)

    wedges, texts, autotexts = ax.pie(data,
                                      autopct=lambda percent: func(percent,
                                                                   data),
                                      textprops=dict(color="w"))

    legend_style = section[LAYOUT_KEY]['legendStyle']

    def get_location(align, vertical_align):
        vertical_align = vertical_align.replace('top', 'upper').replace(
            'bottom', 'lower')
        return f'{vertical_align} {align}'

    ax.legend(wedges, keys,
              title="",
              loc=get_location(legend_style['align'],
                               legend_style['verticalAlign']),
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title(section['title'])
    circle = plt.Circle((0, 0), 0.5, color='white')
    ax.add_artist(circle)

    path = Path(tempfile.mkdtemp()) / Path(
        next(tempfile._get_candidate_names()) + '.png')

    print(str(path))
    plt.savefig(str(path), format='png', bbox_inches='tight')

    with open(str(path), "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8", "ignore")
        b64 = f'data:image/png;base64,{img_base64}'

    s = {
        'type': 'image',
        'data': b64
    }
    image.insert(cell_object, s)

    # with get_temp_fd() as f:
