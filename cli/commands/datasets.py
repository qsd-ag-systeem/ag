import click
from halo import Halo

from core.common import print_table, retrieve_datasets
from core.delete import delete_dataset_by_name, delete_dataset_files_by_name, delete_file_by_name, delete_dataset_file_by_name


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
            f"An error occurred while fetching the datasets{error}", err=True)


@click.command("delete", help="Verwijdert een dataset.")
@click.argument('dataset', type=str)
@click.option('-f', '--file', type=str, default=None)
@click.option('--debug/--no-debug', default=False)
@click.option('--delete-files/--no-delete-files', default=False)
def delete_dataset(dataset: str, file: str, debug: bool, delete_files: bool) -> None:
    """
    This command deletes a dataset.
    """
    spinner = Halo(text=f"Deleting dataset '{dataset}' ...", spinner='dots')
    spinner.start()

    try:
        if file:
            delete_file_by_name(dataset, file)

            if delete_files:
                delete_dataset_file_by_name(dataset, file)
        else:
            delete_dataset_by_name(dataset)

            if delete_files:
                delete_dataset_files_by_name(dataset)

        spinner.succeed(f"Dataset '{dataset}' removed successfully.")
    except Exception as e:
        spinner.fail(f"Deleting dataset '{dataset}' failed.")

        if debug:
            click.echo(e, err=True)

        exit(1)
