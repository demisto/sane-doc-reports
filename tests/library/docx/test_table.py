from docx.table import Table

from sane_doc_reports.report import Report
from tests import utils
from tests.utils import get_mock


def test_table_in_report():
    report = Report(get_mock('docx/table.json'))
    report.populate_report()
    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)
    assert len(table.columns) == 12
    assert len(table.rows) == 1

    # Check that there is indeed an image
    assert len(d.element.xpath('//w:tbl//w:tbl')) == 1

    # Check that it has the right amount of rows
    assert len(d.element.xpath('//w:tbl//w:tbl//w:t')) == 21