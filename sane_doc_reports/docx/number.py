from typing import Dict

from sane_doc_reports.conf import DEBUG
from sane_doc_reports.utils import open_b64_image


def insert(cell_object: Dict, section: Dict) -> None:
    if DEBUG:
        print("Yo I am a number")

