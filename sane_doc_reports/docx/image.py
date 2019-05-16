from sane_doc_reports.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.docx import error
from sane_doc_reports.utils import open_b64_image, has_run


class ImageElement(Element):

    def insert(self):
        if DEBUG:
            print("Adding image...")

        self.cell_object.run.add_picture(
            open_b64_image(self.section.contents))


def invoke(cell_object, section):
    if section.type != 'image':
        section.contents = f'Called image but not image -  [{section}]'
        return error.invoke(cell_object,  section)

    has_run(cell_object)

    ImageElement(cell_object, section).insert()
