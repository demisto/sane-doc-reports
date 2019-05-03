from sane_doc_reports.Element import Element
from sane_doc_reports.utils import open_b64_image


class ImageElement(Element):

    def insert(self):
        print("Adding image...")
        self.cell_object.run.add_picture(
            open_b64_image(self.section.contents))


def invoke(cell_object, section):
    if section.type != 'image':
        raise ValueError('Called image but not image - ', section)

    return ImageElement(cell_object, section).insert()
