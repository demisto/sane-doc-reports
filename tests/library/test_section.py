from tests.utils import get_mock

from sane_doc_reports.Section import sane_to_section


def test_sane_to_section():
    image_json = get_mock('docx/image.json')
    s = sane_to_section(image_json)
    print(s)