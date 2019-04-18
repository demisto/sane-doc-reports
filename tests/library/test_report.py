import pytest
from docx.table import Table

from sane_doc_reports.grid import get_vtable_merged
from sane_doc_reports.report import Report
from tests import utils
from tests.utils import get_mock


def test_creation_of_report_layout_basic():
    report = Report(get_mock('basic.json'))
    report.populate_report()

    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)
    assert len(table.columns) == 12
    assert len(table.rows) == 2

    # Check the specific merged cells
    vtable = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    assert get_vtable_merged(table) == vtable


def test_creation_of_report_layout_full():
    report = Report(get_mock('grid_checks/fullgrid.json'))
    report.populate_report()

    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)
    assert len(table.columns) == 12
    assert len(table.rows) == 12

    # Check the specific merged cells
    vtable = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert get_vtable_merged(table) == vtable


def test_creation_of_report_layout_merged():
    report = Report(get_mock('grid_checks/mergegrid.json'))
    report.populate_report()

    d = report.document
    table = next(utils.iter_block_items(d))
    assert isinstance(table, Table)
    assert len(table.columns) == 12
    assert len(table.rows) == 9

    # Check the specific merged cells
    vtable = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    ]
    assert get_vtable_merged(table) == vtable


def test_markdown_and_text():
    """
        To check the xpath: rename the .docx to .zip and open word/document.xml
    """
    report = Report(get_mock('grid_checks/fullgrid.json'))
    report.populate_report()

    d = report.document

    # Find 4 fonts
    assert len(d.element.xpath('//w:rFonts')) == 4
    assert len(d.element.xpath('//w:rFonts[@w:ascii="Arial"]')) == 4

    # Find one H1
    assert len(d.element.xpath("//w:sz[@w:val='56']")) == 3

    # Find two H2
    assert len(d.element.xpath("//w:sz[@w:val='28']")) == 1

