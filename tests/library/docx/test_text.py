from sane_doc_reports.report import Report
from tests.utils import get_mock


def test_text():
    """
        To check the xpath: rename the .docx to .zip and open word/document.xml
    """
    report = Report(get_mock('docx/text.json'))
    report.populate_report()

    d = report.document

    # Find 1 fonts
    assert len(d.element.xpath('//w:rFonts')) == 1

    # Check with Arial font too
    assert len(d.element.xpath('//w:rFonts[@w:ascii="Arial"]')) == 1

    # Find one H1
    assert len(d.element.xpath('//w:sz[@w:val="48"]')) == 1

    # Find two H2
    assert len(d.element.xpath('//w:sz[@w:val="32"]')) == 1

    # Find styles
    assert len(d.element.xpath('//w:i')) == 1
    assert len(d.element.xpath('//w:strike')) == 1
    assert len(d.element.xpath('//w:u')) == 1
    assert len(d.element.xpath('//w:b')) == 1
