from sane_doc_reports.domain.CellObject import CellObject
from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG, PYDOCX_FONT_SIZE, STYLE_KEY, \
    DEFAULT_TABLE_FONT_SIZE
from sane_doc_reports.domain.Section import Section
from sane_doc_reports.elements import error, image
from sane_doc_reports.populate.utils import insert_text_into_cell


def fix_order(ordered, readable_headers) -> list:
    """ Return the readable headers by the order given """
    temp_readable = {i[0].lower() + i[1:]: i for i in readable_headers}
    # Investigations are not lowercased
    inv_fix = {i: i for i in readable_headers}
    temp_readable = {**temp_readable, **inv_fix}

    ret = []
    for ordered_key in ordered:
        ret.append(temp_readable[ordered_key])
    return ret


class TableElement(Element):

    def insert(self):
        if DEBUG:
            print("Adding table...")

        table_data = self.section.contents
        if 'readableHeaders' in self.section.layout:
            ordered = self.section.layout['tableColumns']
            readable_headers = self.section.layout['readableHeaders'].values()
            table_columns = fix_order(ordered, readable_headers)
        else:
            table_columns = self.section.layout['tableColumns']

        table = self.cell_object.cell.add_table(rows=1, cols=len(table_columns))
        table.style = 'Light Shading'
        hdr_cells = table.rows[0].cells
        text_style = {STYLE_KEY: {PYDOCX_FONT_SIZE: DEFAULT_TABLE_FONT_SIZE}}

        for i, header_text in enumerate(table_columns):
            insert_text_into_cell(hdr_cells[i], header_text, text_style)

        for r in table_data:
            row_cells = table.add_row().cells
            for i, header_text in enumerate(table_columns):
                if header_text in r:

                    # Investigations can have 'Avatars', which are images
                    if isinstance(r, dict) and 'Avatar' in r:
                        r = r['Avatar']
                        s = Section(r['type'], r['data'], {}, {})
                        co = CellObject(row_cells[i], add_run=False)
                        image.invoke(co, s)
                    else:
                        insert_text_into_cell(row_cells[i], r[header_text],
                                          text_style)


def invoke(cell_object, section):
    if section.type != 'table':
        section.contents = f'Called table but not table -  [{section}]'
        return error.invoke(cell_object, section)

    TableElement(cell_object, section).insert()
