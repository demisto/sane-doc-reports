import docx
from docx.enum.dml import MSO_THEME_COLOR_INDEX

from sane_doc_reports.Element import Element
import sane_doc_reports.styles.text as text_style
from sane_doc_reports.conf import DEBUG


def add_hyperlink_into_run(paragraph, run, url):
    runs = paragraph.runs
    for i in range(len(runs)):
        if runs[i].text == run.text:
            break

    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK,
                          is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )
    hyperlink.append(run._r)
    paragraph._p.insert(i + 1, hyperlink)

    # Add the style
    run.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
    run.font.underline = True


class LinkElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding link...')

        self.cell_object.add_run()
        self.cell_object.run.text = self.section.contents

        # Add more text styling
        text_style.apply_style(self.cell_object, self.section)

        add_hyperlink_into_run(self.cell_object.paragraph, self.cell_object.run,
                               self.section.extra['href'])


def invoke(cell_object, section) -> None:
    if section.type not in ['a']:
        raise ValueError('Called link but not link - ', section)

    LinkElement(cell_object, section).insert()
