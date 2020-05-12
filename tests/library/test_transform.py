from sane_doc_reports.conf import ROW_POSITION_KEY, COL_POSITION_KEY, LAYOUT_KEY
from tests.utils import _transform


def test_sane_json_null_values():
    json = _transform('invalid/null_values.json')
    assert json[1].json_data[0][LAYOUT_KEY][ROW_POSITION_KEY] == 0
    assert json[1].json_data[0][LAYOUT_KEY][COL_POSITION_KEY] == 0


def test_sane_json_no_text_in_data():
    json = _transform('invalid/no_text_in_data.json')
    assert 'text' in json[1].json_data[0]['data']


def test_sane_json_json_parse_not_list_table():
    json = _transform('invalid/json_parse_becomes_not_list.json')
    assert isinstance(json[1].json_data[0]['data'], list)


def test_sane_json_no_old_logo_and_badge():
    json = _transform('elements/items_section.json')
    assert 'vXFNR9MceWKm7g2FgwASeuax2lNJUJQ1zRG/isu' in json[2]['customer_logo']
    for item in json[1].json_data:
        data = str(item['data'])
        is_badge = 'PSIzNCIgdmlld0JveD0iMCAwIDM0IDM0Ij4' in data
        is_old_logo = 'TF7ZmlsbDojMzczODNkO30uY2xzLTJ7Zmls' in data
        assert not is_badge and not is_old_logo
