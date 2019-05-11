import click

from sane_doc_reports.Report import Report


@click.command()
@click.argument('input', type=click.Path(exists=True, readable=True))
@click.argument('output', type=click.Path())
def main(input, output):
    report = Report(input)
    report.populate_report()
    report.save(output)

    click.echo('Converted successfully.')


if __name__ == "__main__":
    main()
