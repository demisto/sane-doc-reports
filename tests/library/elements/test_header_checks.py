from docx.table import Table

from sane_doc_reports.conf import XSOAR_LOGO_BASE64
from sane_doc_reports.populate.Report import Report
from tests import utils
from tests.utils import _transform


def test_logo_works_in_regular_report():
    report = Report(*_transform('grid_checks/fullgrid.json'), options={
        'customerLogo': XSOAR_LOGO_BASE64,
        'demistoLogo': XSOAR_LOGO_BASE64
    })
    report.populate_report()
    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)

    # Check headers for 2 images (customer logo)
    assert len(d.sections[0].header._element.xpath('.//w:drawing')) == 2


def test_logo_works_in_regular_report_without_customer_logo():
    report = Report(*_transform('grid_checks/fullgrid.json'), options={
        'customerLogo': None,
        'demistoLogo': XSOAR_LOGO_BASE64
    })
    report.populate_report()
    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)

    # Check headers for 2 images (customer logo)
    assert len(d.sections[0].header._element.xpath('.//w:drawing')) == 1


def test_logo_not_added_if_headers_disabled():
    report = Report(*_transform('grid_checks/fullgrid.json'), options={
        'customerLogo': XSOAR_LOGO_BASE64,
        'demistoLogo': XSOAR_LOGO_BASE64,
        'disableHeaders': True
    })
    report.populate_report()
    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)

    # Check headers for 2 images (customer logo)
    assert len(d.sections[0].header._element.xpath('.//w:drawing')) == 0
