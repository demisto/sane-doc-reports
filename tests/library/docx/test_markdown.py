from sane_doc_reports.Report import Report
from tests.utils import get_mock


def test_markdown():
    """
        To check the xpath: rename the .docx to .zip and open word/document.xml
    """
    report = Report(get_mock('docx/markdown.json'))
    report.populate_report()

    d = report.document

    # Find 6 headings
    assert len(d.element.xpath("//w:t[contains(text(), 'Heading')]")) == 6

    # Find 3 Hrs
    assert len(d.element.xpath('//w:bottom[@w:val="single"]')) == 3

    # Find Text stylings
    #   Two bold
    assert len(d.element.xpath(
        "//w:r//w:t[contains(text(), 'bold')]/preceding-sibling" +
        "::w:rPr/w:b")) == 2
    #   Two italics
    assert len(d.element.xpath(
        "//w:r//w:t[contains(text(), 'italic')]/preceding-sibling" +
        "::w:rPr/w:i")) == 2
    #   One strikethrough
    assert len(d.element.xpath(
        "//w:r//w:t[contains(text(), 'Strike')]/preceding-sibling" +
        "::w:rPr/w:strike")) == 1

    # Find one quote
    assert len(d.element.xpath(
        '//w:tbl//w:shd[@w:fill="#fff8dc"]/following::w:t[position() <2]')) == 1

    # Find one code
    assert len(d.element.xpath(
        '//w:tbl//w:shd[@w:fill="#f5f5f5"]/following::w:t[position() <2]')) == 1

    # Find ULs
    assert len(
        d.element.xpath('//w:p//w:pStyle[contains(@w:val,"ListBullet")]')) == 4

    # Find OLs
    assert len(
        d.element.xpath('//w:p//w:pStyle[contains(@w:val,"ListNumber")]')) == 4

    # Find one link
    assert len(d.element.xpath("//w:hyperlink//w:t[text()='link text']")) == 1

    # Find one image
    assert len(
        d.element.xpath("//w:drawing//pic:cNvPr[@name='image.png']")) == 1