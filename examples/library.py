from sane_doc_reports import main
from sane_doc_reports.populate.Report import Report
from tests.utils import get_mock


def example_basic():
    report = Report(get_mock('grid_checks/fullgrid.json'))
    report.populate_report()
    report.save('example.docx')


def example_table():
    report = Report(get_mock('elements/table.json'))
    report.populate_report()
    report.save('example.docx')


def example_number():
    report = Report(get_mock('elements/number_and_trend.json'))
    report.populate_report()
    report.save('example.docx')


def example_text():
    main.run(get_mock('elements/text.json'), 'example.docx')


def example_pie_chart():
    report = Report(get_mock('elements/pie_chart.json'))
    report.populate_report()
    report.save('example.docx')


def example_markdown():
    report = Report(get_mock('elements/markdown.json'))
    report.populate_report()
    report.save('example.docx')


def example_hr():
    report = Report(get_mock('elements/hr.json'))
    report.populate_report()
    report.save('example.docx')


def example_investigation():
    report = Report(get_mock('elements/investigation.json'))
    report.populate_report()
    report.save('example.docx')


def _example_junk():
    # Generate a big elements file for testing
    report = Report(get_mock('junkbig.json'))
    report.populate_report()
    report.save('example.docx')


def example_bar_chart():
    report = Report(get_mock('elements/bar_chart.json'))
    report.populate_report()
    report.save('example.docx')


def run():
    # Gets the json form tests/mock_data
    example_text()


if __name__ == '__main__':
    run()
