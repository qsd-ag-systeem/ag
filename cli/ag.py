"""
CLI for the face recognition application.
"""
import click
from halo import Halo

from api.app import run as run_api
from cli.commands.cross_search import cross_search
from cli.commands.delete_dataset import delete_dataset
from cli.commands.enroll import enroll
from cli.commands.export_dataset import export_dataset
from cli.commands.get_datasets import get_datasets
from cli.commands.import_dataset import import_dataset
from cli.commands.search import search
from core.setup_db import ensure_db_running, ensure_index_exists


@click.group(help="Dit is de command line interface (CLI) voor het gebruiken van het automatisch gelaat herkenningssysteem")
def cli():
    """
    CLI group for the face recognition application.
    """
    init_app()


@cli.command(help="Start de web applicatie")
@click.option('--host', type=str, default='127.0.0.1', help='Host waarop de web applicatie draait')
@click.option('--port', type=int, default=8080, help='Poort waarop de web applicatie draait')
@click.option('--debug/--no-debug', default=False, help='Debug mode')
def web(host: str, port: int, debug: bool):
    run_api(host, port, debug)


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
        spinner.fail("Failed to initialize application. Is Docker running?")
        click.echo(e, err=True)
        exit(1)

    spinner.stop()


cli.add_command(enroll)
cli.add_command(search)
cli.add_command(get_datasets)
cli.add_command(delete_dataset)
cli.add_command(export_dataset)
cli.add_command(import_dataset)
cli.add_command(cross_search)


if __name__ == '__main__':
    cli()
