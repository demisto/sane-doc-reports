from sane_doc_reports.Report import Report
from tests.utils import get_mock


def example_basic():
    report = Report(get_mock('grid_checks/fullgrid.json'))
    report.populate_report()
    report.save('example.docx')


def example_table():
    report = Report(get_mock('docx/table.json'))
    report.populate_report()
    report.save('example.docx')


def example_number():
    report = Report(get_mock('docx/number_and_trend.json'))
    report.populate_report()
    report.save('example.docx')


def example_text():
    report = Report(get_mock('docx/text.json'))
    report.populate_report()
    report.save('example.docx')


def example_pie_chart():
    report = Report(get_mock('docx/pie_chart.json'))
    report.populate_report()
    report.save('example.docx')


def example_markdown():
    report = Report(get_mock('docx/markdown.json'))
    report.populate_report()
    report.save('example.docx')


def example_investigation():
    report = Report(get_mock('docx/markdown.json'))
    report.populate_report()
    report.save('example.docx')


def example_junk():
    report = Report(get_mock('junkbig.json'))
    report.populate_report()
    report.save('example.docx')


def main():
    # Gets the json form tests/mock_data
    # example_investigation()
    # example_markdown()
    example_markdown()


if __name__ == '__main__':
    main()
