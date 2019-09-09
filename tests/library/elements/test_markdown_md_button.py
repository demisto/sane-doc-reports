from sane_doc_reports import conf
from sane_doc_reports.populate.Report import Report
from tests.utils import _transform


def test_markdown_md_button():
    report = Report(*_transform('elements/markdown_md_button.json'))
    report.populate_report()

    d = report.document

    # Find 6 headings
    assert len(d.element.xpath("//w:t[contains(text(), '%')]")) == 0
    assert len(d.element.xpath("//w:t[contains(text(), 'hi 1')]")) == 1

