from datetime import datetime

from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG, LAYOUT_KEY
from sane_doc_reports.domain.Section import Section
from sane_doc_reports.elements import error, text


class DateElement(Element):
    """ Mainly used to fix the investigation date element """

    def insert(self):
        if DEBUG:
            print('Adding text...')

        today = datetime.now()
        default_date_format = '%m %b %Y %H:%M:%S %SZ'

        if not self.section.contents:
            formatted_date = today.strftime(default_date_format)

        elif LAYOUT_KEY in self.section.contents:
            layout = self.section.contents[LAYOUT_KEY]
            date_string = self.section.contents
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

            if "format" in layout:
                formatted_date = date.strftime(layout["format"])
            else:
                formatted_date = date.strftime(default_date_format)

        section = Section('text', formatted_date, {}, {})
        text.invoke(self.cell_object, section)


def invoke(cell_object, section) -> None:
    if section.type != 'date':
        section.contents = f'Called date but not date -  [{section}]'
        return error.invoke(cell_object, section)

    DateElement(cell_object, section).insert()
