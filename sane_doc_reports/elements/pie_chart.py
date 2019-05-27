import matplotlib.pyplot as plt

from sane_doc_reports.domain.Section import Section
from sane_doc_reports.conf import DEBUG

from sane_doc_reports.elements import image, error
from sane_doc_reports.utils import get_ax_location
from sane_doc_reports.styles.colors import get_colors
from sane_doc_reports import utils
from sane_doc_reports.domain.Element import Element


class PieChartElement(Element):

    @utils.plot
    def insert(self):
        if DEBUG:
            print('Adding pie chart: ...')
        size_w, size_h, dpi = utils.convert_plt_size(self.section)
        fig, ax = plt.subplots(figsize=(size_w, size_h), dpi=dpi,
                               subplot_kw=dict(aspect="equal"))

        data = [int(i['data'][0]) for i in self.section.contents]
        objects = [i['name'] for i in self.section.contents]

        # Fix the unassigned key:
        objects = [i if i != "" else "Unassigned" for i in objects]

        # Generate the default colors
        colors = get_colors(self.section.layout, objects)
        unassigned_color = 'darkgrey'

        # If we have predefined colors, use them
        if 'legend' in self.section.layout and self.section.layout['legend']:
            colors = [i['color'] for i in self.section.layout['legend']]

        color_keys = {}
        for i, k in enumerate(objects):
            color_keys[k] = colors[i]
            if k == 'Unassigned':
                color_keys['Unassigned'] = unassigned_color

        final_colors = [color_keys[k] for k in objects]

        wedges, texts = ax.pie(data,
                               colors=final_colors,
                               startangle=90, pctdistance=0.85,
                               textprops=dict(color="w"))

        keys_with_numbers = ['{}: {}'.format(k, data[i]) for i, k in
                             enumerate(objects)]

        legend_location_relative_to_graph = (1, 0, 0.5, 1)
        legend_style = self.section.layout['legendStyle']
        ax.legend(wedges, keys_with_numbers,
                  title="",
                  loc=get_ax_location(legend_style),
                  bbox_to_anchor=legend_location_relative_to_graph
                  )

        ax.set_title(self.section.extra['title'])
        circle = plt.Circle((0, 0), 0.5, fc='white')
        ax.add_artist(circle)

        plt_b64 = utils.plt_t0_b64(plt)

        s = Section('image', plt_b64, {}, {})
        image.invoke(self.cell_object, s)


def invoke(cell_object, section):
    if section.type != 'pie_chart':
        section.contents = f'Called pie_chart but not pie_chart - [{section}]'
        return error.invoke(cell_object, section)

    PieChartElement(cell_object, section).insert()
