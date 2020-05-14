from docx.table import Table
from datetime import date

from sane_doc_reports.populate.Report import Report
from tests import utils
from tests.utils import _transform


def test_items_section_in_report():
    report = Report(*_transform('elements/header_svg.json'))
    report.populate_report()
    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)

    # Check headers for 2 images (customer logo)
    assert len(d.sections[0].header._element.xpath('.//w:drawing')) == 2
