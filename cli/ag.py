import click
import os
from core.face_recognition import folder_enroll, folder_search, retrieve_datasets
from core.setup_db import setup_db


@click.group()
def cli():
    pass


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
def enroll(folder: str, debug: bool) -> None:
    folder_path = os.path.abspath(os.curdir + "/" + folder)
    folder_enroll(folder, folder_path, debug)
    click.echo('Enrollment finished!')


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option("--dataset", "-d", "dataset", type=str, required=False, multiple=True, help="De naam van een bestaande dataset. In het geval dat bij de enrollment een naam is gekozen anders dan de folder naam kan ook de folder naam alsnog gebruikt worden bij het verwijderen.")
def search(folder: str, dataset: str, list) -> None:
    click.echo(f'Search: {dataset}')
    print(folder_search(folder, dataset))

@cli.command()
def list() -> None:
    print(retrieve_datasets())

@cli.command()
def setup() -> None:
    setup_db()
    click.echo(f'Done')


@cli.command()
def test() -> None:
    click.echo(f'Test!')
