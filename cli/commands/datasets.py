import click
from core.common import print_table
from core.search import retrieve_datasets, delete_dataset


@click.command("datasets", help="Geeft een lijst met alle beschikbare datasets.")
@click.option('--debug/--no-debug', default=False)
def get(debug: bool) -> None:
    """
    This command lists all available datasets.
    """
    try:
        rows = retrieve_datasets()
        print_table(["Name", "Enrolled images"], rows)
    except Exception as err:
        error = f": {err}" if debug else ""
        click.echo(
            f"An error occurred while fetching the datasets{error}", err=True)


@click.command("delete", help="Verwijdert een dataset.")
@click.argument('dataset', type=str)
@click.option('--debug/--no-debug', default=False)
@click.option('--delete-files/--no-delete-files', default=False)
def delete(dataset: str, debug: bool, delete_files: bool) -> None:
    """
    This command deletes a dataset.
    """
    try:
        delete_dataset(dataset, delete_files)
        click.echo(f"Dataset \"{dataset}\" removed successfully")
    except Exception as err:
        error = f": {err}" if debug else ""
        click.echo(
            f"An error occurred while deleting the dataset{error}", err=True)