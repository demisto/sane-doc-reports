from sane_doc_reports.Element import Element


class ImageElement(Element):

    def insert(self):
        print("Adding image: ", self.section.contents)


def invoke(cell_object, section):
    if section.type != 'image':
        raise ValueError('Called image but not image - ', section)

    return ImageElement(cell_object, section).insert()

# def insert(cell_object: Dict, section: Dict) -> None:
#     if DEBUG:
#         print("Yo Im image")
#
#     cell_object['run'].add_picture(open_b64_image(section['data']))
