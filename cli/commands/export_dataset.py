from pathlib import Path
import click
import os

from halo import Halo
from slugify import slugify

from core.common import dataset_exists
from core.export_dataset import export_datasets, export_datasets_by_name


@click.command("export", help="Exporteert een csv bestand van één of meerdere specifieke datasets uit de database.")
@click.argument('file_name', type=str)
@click.option("--dataset", "-d", "datasets", type=str, required=False, multiple=True, help="Kan meerdere keren gebruikt worden. De naam van een dataset waarin gezocht word. Als er geen dataset wordt aangegeven worden alle beschikbare datasets gebruikt.")
@click.option('--debug/--no-debug', default=False)
def export_dataset(file_name: str, datasets: tuple, debug: bool) -> None:
    """
    Exports a csv file from a specific or multiple datasets from the database.
    """
    output_dir = os.path.abspath(os.path.join(os.getcwd(), "output"))
    file_path = os.path.join(output_dir, f"{slugify(file_name)}.csv")

    if debug:
        click.echo(f"Output directory: {output_dir}")
        click.echo(f"File path: {file_path}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    spinner = Halo(text=f"Exporting to '{file_path}' ...", spinner='dots')
    spinner.start()

    if Path(file_path).is_file():
        spinner.fail(f"Export to '{file_path}' failed.")
        click.echo("Error: a file with this name already exists.", err=True)
        exit(1)

    for dataset in datasets:
        if not dataset_exists(dataset):
            spinner.fail(f"Export to '{file_path}' failed.")
            click.echo(f"Dataset '{dataset}' does not exist.", err=True)
            exit(1)

    try:
        if not datasets:
            export_datasets(file_path)
        else:
            export_datasets_by_name(file_path, datasets)
    except Exception as e:
        spinner.fail(f"Export to '{file_path}' failed.")
        click.echo(f"Error: {e}", err=True)
        exit(1)

    spinner.succeed(f"Export to '{file_path}' complete.")
