import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from sane_doc_reports import utils
from sane_doc_reports.Element import Element
from sane_doc_reports.Section import Section
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.docx import image
from sane_doc_reports.utils import get_ax_location


class LineChartElement(Element):

    @utils.plot
    def insert(self):
        if DEBUG:
            print("Adding line chart...")

        # Fix sizing
        size_w, size_h, dpi = utils.convert_plt_size(self.section)
        figure(num=2, figsize=(size_w, size_h), dpi=dpi)

        data = self.section.contents

        # Make the groups look like:
        # groups = {
        #   'Type A': {
        #       dates: ['2000', '2001', '2002']
        #       values: ['1', '2', '3']
        #    }
        #   'Type B': {
        #         dates: ['2000', '2001', '2002'],
        #         values : ['4', '5', '6']
        # }
        groups = {}
        for date_group in data:
            for line in date_group['groups']:
                if line['name'] not in groups:
                    groups[line['name']] = {
                        'dates': [date_group['name']],
                        'values': [line['data'][0]]
                    }
                    continue
                groups[line['name']]['dates'].append(date_group['name'])
                groups[line['name']]['values'].append(line['data'][0])

        legend_colors = {i['name']: i['color'] for i in self.section.layout['legend']}

        # Plot the lines
        for group, line in groups.items():
            x_axis = line['dates']
            y_axis = line['values']
            plt.plot(x_axis, y_axis, marker='', color=legend_colors[group],
                     linewidth=2)

        # Add the legend
        legend_style = self.section.layout['legendStyle']
        plt.legend([i for i in groups.keys()], loc=get_ax_location(legend_style))

        # Add to docx as image
        plt_b64 = utils.plt_t0_b64(plt)
        s = Section('image', plt_b64, {}, {})
        image.invoke(self.cell_object, s)


def invoke(cell_object, section):
    if section.type != 'line_chart':
        raise ValueError('Called line_chart but not line_chart - ', section)

    return LineChartElement(cell_object, section).insert()
