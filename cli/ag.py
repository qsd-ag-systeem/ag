import click
import os
import dlib
from core.face_recognition import init, process_file
from core.setup_db import setup_db
from pathlib import Path


@click.group()
def cli():
    pass


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
@click.option('--cuda/--no-cuda', default=True)
def enroll(folder: str, debug: bool, cuda: bool) -> None:
    folder_path = os.path.abspath(os.curdir + "/" + folder)

    files = list((x for x in Path(folder_path).iterdir() if x.is_file()))
    errors = []

    init(cuda)

    if dlib.DLIB_USE_CUDA and cuda:
        print("⚡ Using CUDA!")
    else:
        print("🐢 CUDA not available, falling back to CPU processing!")

    with click.progressbar(files, show_pos=True, show_percent=True, label="Initializing...") as bar:
        for file in bar:
            try:
                process_file(folder, file)
                bar.label = f"Processing: {os.path.relpath(file)}"
            except Exception as error:
                bar.label = f"Error processing: {os.path.relpath(file)}"

                if debug:
                    errors.append(error)

                pass

    for error in errors:
        click.echo(error)

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
