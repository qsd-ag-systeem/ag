from pathlib import Path

import click
import os

from slugify import slugify
from core.export_dataset import export_all, export_dataset


@click.command()
@click.argument('file_name', type=str)
@click.option("--dataset", "-d", "dataset", type=str, required=False, multiple=True, help="Kan meerdere keren gebruikt worden. De naam van een dataset waarin gezocht word. Als er geen dataset wordt aangegeven worden alle beschikbare datasets gebruikt.")
@click.option('--debug/--no-debug', default=False)
def export(file_name: str, dataset: tuple, debug: bool) -> None:
    output_dir = os.path.abspath(os.path.join(os.getcwd(), "output"))
    file_path = os.path.join(output_dir, f"{slugify(file_name)}.csv")

    if debug:
        click.echo(f"Output directory: {output_dir}")
        click.echo(f"File path: {file_path}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if Path(file_path).is_file():
        click.echo("Error: a file with this name already exists.", err=True)
        return

    if debug:
        click.echo(f"Exporting to {file_path}")

    if not dataset:
        export_all(file_path)
    else:
        export_dataset(file_path, dataset)

    click.echo(f'Done')