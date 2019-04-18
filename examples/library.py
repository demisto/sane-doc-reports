from sane_doc_reports.report import Report
from tests.utils import get_mock


def main():
    # Gets the json form tests/mock_data
    report = Report(get_mock('fullgrid.json'))
    report.populate_report()
    report.save('example.docx')


if __name__ == '__main__':
    main()
