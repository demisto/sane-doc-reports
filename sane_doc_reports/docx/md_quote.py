from sane_doc_reports.Wrapper import Wrapper


class QuoteWrapper(Wrapper):
    def insert(self):
        print("inserting a quote wrapper")


'''
def insert(cell_object: Dict, section) -> Dict:
    """ This is a special function, we only make the cell background and
     continue to add elements here """
    if DEBUG:
        print("Yo I am markdown generated quote!")

    new_cell = cell_object['cell'].add_table(1, 1).cell(0, 0)
    # Background color
    shading_elm_1 = parse_xml(
        f'<w:shd {{}} w:fill="{name_to_hex("cornsilk")}"/>'.format(
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
