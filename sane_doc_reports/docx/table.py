from typing import Dict

from sane_doc_reports.conf import DEBUG, LAYOUT_KEY


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print('Yo I am a table')

    table_data = section['data']

    if 'readableHeaders' in section[LAYOUT_KEY]:
        table_columns = list(section[LAYOUT_KEY]['readableHeaders'].values())
    else:
        table_columns = section[LAYOUT_KEY]['tableColumns']

    table = cell_object['cell'].add_table(rows=1, cols=len(table_columns))
    table.style = 'Light Shading'
    hdr_cells = table.rows[0].cells

    for i, header in enumerate(table_columns):
        hdr_cells[i].text = header

    for r in table_data:
        row_cells = table.add_row().cells
        for i, header in enumerate(table_columns):
            if header in r:
                row_cells[i].text = r[header]