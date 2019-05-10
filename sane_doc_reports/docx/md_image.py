import base64

import requests

from sane_doc_reports.Element import Element
from sane_doc_reports.Section import Section
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.docx import image


def image_contents_from_url(url):
    r = requests.get(url, verify=False)
    return "data:" + \
           r.headers['Content-Type'] + ";" + \
           "base64," + str(base64.b64encode(r.content).decode("utf-8"))


class ExternalImageElement(Element):

    def insert(self):
        if DEBUG:
            print('Adding md image...')

        url = self.section.extra['src']
        image_data = image_contents_from_url(url)
        img_section = Section('image', image_data, {}, {})
        image.invoke(self.cell_object, img_section)


def invoke(cell_object, section) -> None:
    if section.type not in ['img']:
        raise ValueError('Called image but not image - ', section)

    ExternalImageElement(cell_object, section).insert()
