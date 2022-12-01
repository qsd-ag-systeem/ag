import click
import os
from core.face_recognition import init, process_file
from core.setup_db import setup_db
from pathlib import Path


@click.group()
def cli():
    pass


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
def enroll(folder: str, debug: bool) -> None:
    folder_path = os.path.abspath(os.curdir + "/" + folder)

    files = list((x for x in Path(folder_path).iterdir() if x.is_file()))

    with click.progressbar(files, label="Initializing...") as bar:
        init()

        for file in bar:
            process_file(folder, file, debug)
            try:
                bar.label = f"Processing: {os.path.relpath(file)}"
            except Exception as error:
                bar.label = f"Error processing: {os.path.relpath(file)}"

                if debug:
                    print(error)

                pass

    click.echo('Enrollment finished!')


@cli.command()
@click.option("--dataset", "-ad", "dataset", type=str, required=True, help="De naam van een bestaande dataset. In het geval dat bij de enrollment een naam is gekozen anders dan de folder naam kan ook de folder naam alsnog gebruikt worden bij het verwijderen.")
def search(dataset: str) -> None:
    click.echo(f'Search: {dataset}')


@cli.command()
def setup() -> None:
    setup_db()
    click.echo(f'Done')


@cli.command()
def test() -> None:
    click.echo(f'Test!')
