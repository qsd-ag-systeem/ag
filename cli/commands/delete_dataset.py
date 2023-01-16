import click
from halo import Halo

from core.delete import delete_dataset_by_name, delete_dataset_files_by_name, delete_file_by_name, delete_dataset_file_by_name

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
