"""
CLI for the face recognition application.
"""
import click
from halo import Halo

from core.setup_db import ensure_index_exists, ensure_db_running
from cli.commands.enroll import enroll
from cli.commands.search import search
from cli.commands.datasets import delete_dataset, get_datasets
from cli.commands.export_dataset import export_dataset
from cli.commands.import_dataset import import_dataset


@click.group(help="Dit is de command line interface (CLI) voor het gebruiken van het automatisch gelaat herkenningssysteem")
def cli():
    """
    CLI group for the face recognition application.
    """
    init_app()

@cli.command(hidden=True)
def setup():
    init_app()


def init_app():
    spinner = Halo(text='Initializing application ...', spinner='dots')
    spinner.start()

    try:
        ensure_db_running()
        ensure_index_exists()
    except Exception as e:
        spinner.fail("Failed to initialize application.")
        click.echo(e, err=True)
        exit(1)

    spinner.stop()


cli.add_command(enroll)
cli.add_command(search)
cli.add_command(get_datasets)
cli.add_command(delete_dataset)
cli.add_command(export_dataset)
cli.add_command(import_dataset)


if __name__ == '__main__':
    cli()
