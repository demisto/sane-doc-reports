from pathlib import Path

from sane_doc_reports.cli import main
from click.testing import CliRunner


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Show this message and exit' in result.output


def test_cli_bad_input():
    runner = CliRunner()
    result = runner.invoke(main, ['derp'])
    assert result.exit_code == 2
    result = runner.invoke(main, ['', 'merp'])
    assert result.exit_code == 2
    result = runner.invoke(main, ['derp', 'merp'])
    assert result.exit_code == 2


def test_cli_creating_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.json', 'w') as f:
            f.write('''[{ "type": "text", "data": { "text": "Test"},
                "layout": { "columnPos": 0, "h": 1, "rowPos": 0, "w": 12 }}]''')

        result = runner.invoke(main, ['test.json', 'out.docx'])
        assert result.exit_code == 0
        assert result.output == 'Converted successfully.\n'
        assert Path('out.docx').is_file()
