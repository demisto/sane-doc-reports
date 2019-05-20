from sane_doc_reports import main
from sane_doc_reports.populate.Report import Report
from tests.utils import get_mock


def example_basic():
    main.run(get_mock('grid_checks/fullgrid.json'), 'example.docx')


def example_table():
    main.run(get_mock('elements/table.json'), 'example.docx')


def example_number():
    main.run(get_mock('elements/number_and_trend.json'), 'example.docx')


def example_text():
    main.run(get_mock('elements/text.json'), 'example.docx')


def example_pie_chart():
    main.run(get_mock('elements/pie_chart.json'), 'example.docx')


def example_markdown():
    main.run(get_mock('elements/markdown.json'), 'example.docx')


def example_hr():
    main.run(get_mock('elements/hr.json'), 'example.docx')


def example_investigation():
    main.run(get_mock('elements/investigation.json'), 'example.docx')


def _example_junk():
    # Generate a big elements file for testing
    main.run(get_mock('junkbig.json'), 'example.docx')


def example_bar_chart():
    main.run(get_mock('elements/bar_chart.json'), 'example.docx')


def run():
    # Gets the json form tests/mock_data
    example_markdown()


if __name__ == '__main__':
    run()
