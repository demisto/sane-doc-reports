from typing import Dict

from sane_doc_reports import utils
from sane_doc_reports.conf import DEBUG, DATA_KEY, LAYOUT_KEY

# Plot
import matplotlib.pyplot as plt

from sane_doc_reports.docx import image


def get_ax_location(align, vertical_align):
    vertical_align = vertical_align.replace('top', 'upper').replace(
        'bottom', 'lower')
    return f'{vertical_align} {align}'


@utils.plot
def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("I'm a pie chart")

    size_w, size_h, dpi = utils.convert_plt_size(section)
    fig, ax = plt.subplots(figsize=(size_w, size_h), dpi=dpi,
                           subplot_kw=dict(aspect="equal"))

    data = [int(i['data'][0]) for i in section[DATA_KEY]]
    keys = [i['name'] for i in section[DATA_KEY]]

    # Fix the unassigned key:
    keys = [i if i != "" else "Unassigned" for i in keys]

    # Generate the default colors
    colors = [utils.get_chart_color(i) for i in keys]
    unassigned_color = 'darkgrey'

    # If we have predefined colors, use them
    if 'legend' in section[LAYOUT_KEY] and section[LAYOUT_KEY]['legend']:
        colors = [i['color'] for i in section[LAYOUT_KEY]['legend']]

    color_keys = {}
    for i, k in enumerate(keys):
        color_keys[k] = colors[i]
        if k == 'Unassigned':
            color_keys['Unassigned'] = unassigned_color

    final_colors = [color_keys[k] for k in keys]

    wedges, texts = ax.pie(data,
                           colors=final_colors,
                           startangle=90, pctdistance=0.85,
                           textprops=dict(color="w"))

    legend_style = section[LAYOUT_KEY]['legendStyle']

    keys_with_numbers = ['{}: {}'.format(k, data[i]) for i, k in
                         enumerate(keys)]
    ax.legend(wedges, keys_with_numbers,
              title="",
              loc=get_ax_location(legend_style['align'],
                                  legend_style['verticalAlign']),
              bbox_to_anchor=(1, 0, 0.5, 1)
              )

    ax.set_title(section['title'])
    circle = plt.Circle((0, 0), 0.5, fc='white')
    ax.add_artist(circle)

    plt_b64 = utils.plt_t0_b64(plt)

    s = {
        'type': 'image',
        'data': plt_b64
    }
    image.insert(cell_object, s)
