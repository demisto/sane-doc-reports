from typing import Dict

from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG, DATA_KEY


class TextElement(Element):

    def insert(self):
        print(self)
        print("Adding text: ", self.section.contents)


def invoke(cell_object, section) -> None:
    TextElement(cell_object, section).insert()


# def insert(cell_object: Dict, section: Dict) -> None:
#     if DEBUG:
#         print("Yo I am text!")
#
#     run = cell_object['run']
#     run.text = section[DATA_KEY]['text']
