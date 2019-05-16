from typing import Tuple, Union

from docx.text.paragraph import Paragraph
from docx.text.run import Run


class CellObject(object):
    """ An object containning a cell and it's inner:
     - paragraph (holds: runs (w:p element))
     - run (holds: text, pictures, text-styling (font))
     """

    def __init__(self, cell):
        self.cell = cell

        cell_paragraph, cell_run = self._get_cell_wrappers()
        self.paragraph = cell_paragraph
        self.run = cell_run

    def _get_cell_wrappers(self, add_run=True) -> Tuple[Paragraph,
                                                        Union[Run, None]]:
        """
        Return the cell's paragraph and create a run object too, return them
        both. They are used to inject elements into the table cell.
        Run object:
        - https://python-docx.readthedocs.io/en/latest/api/text.html#run-objects
        Paragraph Object:
        - https://python-docx.readthedocs.io/en/latest/api/text.html#paragraph-objects
        """
        paragraphs = self.cell.paragraphs
        paragraph = paragraphs[0]
        run = None
        if add_run:
            run = paragraph.add_run()
        return paragraph, run
