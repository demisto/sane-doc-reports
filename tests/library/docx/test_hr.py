from sane_doc_reports.Report import Report
from tests.utils import get_mock


def test_hr():
    """
        To check the xpath: rename the .docx to .zip and open word/document.xml
    """
    report = Report(get_mock('docx/hr.json'))
    report.populate_report()

    d = report.document

    # Find 3 paragraphs
    assert len(d.element.xpath('//w:p')) == 3

    # Find hr
    assert len(d.element.xpath('////w:bottom')) == 1

