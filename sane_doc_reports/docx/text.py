from typing import Dict

from sane_doc_reports.conf import DEBUG, DATA_KEY


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am text!")

    run = cell_object['run']
    run.text = section[DATA_KEY]['text']
