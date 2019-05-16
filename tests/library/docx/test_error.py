from sane_doc_reports.Report import Report
from tests.utils import get_mock


def test_text():
    """
        To check the xpath: rename the .docx to .zip and open word/document.xml
    """

    # NOTE: UN COMMENT THIS WHEN YOU HAVE ACTIVE WRAPPERS THAT
    # CAN BREAK THE TYPES

    # report = Report(get_mock('docx/error.json'))
    # report.populate_report()
    #
    # d = report.document
    #
    # # Find 1 fonts
    # assert len(d.element.xpath('//w:rFonts')) == 1
    #
    # # Find an error size
    # assert len(d.element.xpath('//w:sz[@w:val="20"]')) == 1
    #
    # # Find  no H1
    # assert len(d.element.xpath('//w:sz[@w:val="48"]')) == 0
    #
    # # Find no H2
    # assert len(d.element.xpath('//w:sz[@w:val="32"]')) == 0
    #
    # # Find styles
    # assert len(d.element.xpath('//w:i')) == 0
    # assert len(d.element.xpath('//w:strike')) == 0
    # assert len(d.element.xpath('//w:u')) == 0
    # assert len(d.element.xpath('//w:b')) == 2
