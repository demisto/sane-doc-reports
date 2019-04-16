from typing import Dict

from sane_doc_reports.conf import DEBUG


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo Im pie chart")
