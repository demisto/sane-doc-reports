from typing import Dict

from sane_doc_reports.conf import DEBUG, DATA_KEY, LAYOUT_KEY, STYLE_KEY


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am text!")

    cell = cell_object['run']
    paragraph = cell_object['paragraph']

    cell.text = section[DATA_KEY]['text']
