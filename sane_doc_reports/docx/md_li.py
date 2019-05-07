from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from sane_doc_reports.CellObject import CellObject
from sane_doc_reports.MarkdownSection import MarkdownSection
from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.docx import markdown
from sane_doc_reports.utils import name_to_hex


class LiWrapper(Wrapper):

    def wrap(self):
        print("Li...")
        if isinstance(self.section.contents, str):
            self.cell_object.run.add_text(self.section.contents)
            return

        temp_section = MarkdownSection('markdown', self.section.contents, {},
                                       {})
        markdown.invoke(self.cell_object, temp_section,
                        invoked_from_wrapper=True)


def invoke(cell_object, section):
    if section.type != 'li':
        raise ValueError('Called li but not li - ', section)

    return LiWrapper(cell_object, section).wrap()


'''
def insert(cell_object: Dict, section) -> Dict:
    """ This is a special function, we only make the cell background and
     continue to add elements here """
    if DEBUG:
        print("Yo I am markdown generated quote!")

    new_cell = cell_object['cell'].add_table(1, 1).cell(0, 0)
    # Background color
    shading_elm_1 = parse_xml(
        f'<w:shd {{}} w:fill="{name_to_hex("whitesmoke")}"/>'.format(
            nsdecls('w')))
    new_cell._tc.get_or_add_tcPr().append(shading_elm_1)

    cell_paragraph, cell_run = get_cell_wrappers(new_cell)

    new_cell_object = {
        'cell': new_cell,
        'paragraph': cell_paragraph,
        'run': cell_run
    }
    return new_cell_object
'''