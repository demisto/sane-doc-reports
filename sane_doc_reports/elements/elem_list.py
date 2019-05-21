from sane_doc_reports.domain import CellObject, Section
from sane_doc_reports.domain.Wrapper import Wrapper
from sane_doc_reports.elements import error


class ElemListWrapper(Wrapper):
    """ Mainly used to fix the investigation globalSection """

    def wrap(self, invoked_from_wrapper=False):
        # Handle called from another wrapper.
        # if isinstance(self.section.contents, list):
        section_list = self.section.contents

        if not isinstance(section_list, list):
            print(section_list)
            raise ValueError('Elem list does not have valid contents ' +
                             '(must be a list)')


def invoke(cell_object: CellObject, section: Section,
           invoked_from_wrapper=False):
    if section.type != 'elem_list':
        section.contents = f'Called elem_list but not elem_list -  [{section}]'
        return error.invoke(cell_object, section)

    ElemListWrapper(cell_object, section).wrap(
        invoked_from_wrapper=invoked_from_wrapper)
