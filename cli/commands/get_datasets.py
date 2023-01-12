import click

from core.common import print_table, retrieve_datasets


@click.command("datasets", help="Geeft een lijst met alle beschikbare datasets weer.")
@click.option('--debug/--no-debug', default=False)
def get_datasets(debug: bool) -> None:
    """
    This command lists all available datasets.
    """
    try:
        data = retrieve_datasets()
        rows = []

        for dataset in data:
            rows.append([dataset["key"], dataset["doc_count"]])

        print_table(["Name", "Enrolled images"], rows)
    except Exception as err:
        error = f": {err}" if debug else ""
        click.echo(
            f"An error occurred while fetching the datasets{error}",
            err=True
        )
