from sane_doc_reports.Wrapper import Wrapper
from sane_doc_reports.docx import error


class CodeWrapper(Wrapper):

    def wrap(self):
        print("Wrapping code: ", self.section.contents)


def invoke(cell_object, section):
    if section.type != 'code':
        section.contents = f'Called code but not code -  [{section}]'
        return error.invoke(cell_object,  section)

    CodeWrapper(cell_object, section).wrap()

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