import moment

from sane_doc_reports.domain.Element import Element
from sane_doc_reports.conf import DEBUG
from sane_doc_reports.elements import error
from sane_doc_reports.populate.utils import insert_text


class DateElement(Element):
    """ Mainly used to fix the old json's date element """

    def insert(self):
        if DEBUG:
            print('Adding text...')

        default_date_format = '%m %b %Y %H:%M:%S %SZ'

        formatted_date = 'N/A'
        date = moment.now()

        # If no value use current time.
        if self.section.contents == '':
            date = moment.now().strftime(default_date_format)

        # Use the contents
        elif self.section.contents:
            date = moment.date(self.section.contents)

        # If we faild to parse, return 'n/a'
        if not date:
            date = 'n/a'
            insert_text(self.cell_object, date)
            return

        # Use the user supplied format
        if self.section.layout:
            layout = self.section.layout

            if 'format' in layout:
                formatted_date = date.format(layout['format'])
            else:
                formatted_date = date.strftime(default_date_format)
        else:
            formatted_date = date

        insert_text(self.cell_object, formatted_date)


def invoke(cell_object, section) -> None:
    if section.type != 'date':
        section.contents = f'Called date but not date -  [{section}]'
        return error.invoke(cell_object, section)

    DateElement(cell_object, section).insert()
