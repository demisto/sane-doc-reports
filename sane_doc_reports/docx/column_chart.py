from typing import Dict

from sane_doc_reports import utils
from sane_doc_reports.Element import Element
from sane_doc_reports.Section import Section
from sane_doc_reports.conf import DEBUG, DATA_KEY, DEFAULT_BAR_WIDTH, \
    DEFAULT_ALPHA, LAYOUT_KEY, DEFAULT_BAR_ALPHA

import matplotlib.pyplot as plt

from sane_doc_reports.docx import image
from sane_doc_reports.utils import get_ax_location, get_colors


class ColumnChartElement(Element):

    @utils.plot
    def insert(self) -> None:
        """
        This is a standing barchart (bar goes up)
        """
        if DEBUG:
            print("Yo I am column chart!")

        # Fix sizing
        size_w, size_h, dpi = utils.convert_plt_size(self.section)
        plt.figure(figsize=(size_w, size_h), dpi=dpi)

        data = self.section.contents
        objects = [i['name'] for i in data]

        y_axis = [i for i in range(len(objects))]
        x_axis = [i['data'][0] for i in data]

        colors = get_colors(self.section.layout, objects)

        rects = plt.bar(y_axis, x_axis, align='center', alpha=DEFAULT_BAR_ALPHA,
                        width=DEFAULT_BAR_WIDTH, color=colors)

        ax = plt.gca()

        # Fix the legend values to be "some_value (some_number)" instead of
        # just "some_value"
        fixed_legends = [f'{v} ({x_axis[i]})' for i, v in enumerate(objects)]

        legend_style = self.section.layout['legendStyle']
        ax.legend(rects, fixed_legends,
                  loc=get_ax_location(legend_style)).get_frame().set_alpha(
            DEFAULT_ALPHA)
        ax.set_xlim(-len(objects), len(objects))

        plt.xticks(y_axis, objects)
        plt.title(self.section.extra['title'])

        plt_b64 = utils.plt_t0_b64(plt)

        s = Section('image', plt_b64, {}, {})
        image.invoke(self.cell_object, s)


def invoke(cell_object, section):
    if section.type != 'column_chart':
        raise ValueError('Called column_chart but not column_chart - ', section)

    return ColumnChartElement(cell_object, section).insert()
