import click
import os
import cv2
from core.search import retrieve_datasets, retrieve_data, print_results
from core.face_recognition import init, process_file, get_face_embeddings, use_cuda
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

    cuda = use_cuda(cuda)
    init(cuda)

    print("⚡ Using CUDA!" if cuda else "🐢 CUDA not available, falling back to CPU processing!")

    if len(files) == 0:
        click.echo(f"Folder {folder} is empty!")
        return

    with click.progressbar(files, show_pos=True, show_percent=True, label="Initializing...") as bar:
        for file in bar:
            try:
                process_file(folder, file, cuda)
                bar.label = f"Processing: {os.path.relpath(file)}"
            except Exception as error:
                bar.label = f"Error processing: {os.path.relpath(file)}"

                if debug:
                    errors.append(error)

                pass

    for error in errors:
        click.echo(error)

    click.echo('Enrollment finished!')


@cli.command(help="Zoekt een gelijkend gezicht in de database van de meegegeven foto(s)")
@click.argument('folder', type=click.Path(exists=True))
@click.option("--dataset", "-d", "dataset", type=str, required=False, multiple=True, help="Kan meerdere keren gebruikt worden. De naam van een dataset waarin gezocht word. Als er geen dataset wordt aangegeven worden alle beschikbare datasets gebruikt.")
@click.option("--limit", "-l", "limit", type=int, required=False, default=10, help="Het maximaal aantal matches dat tegelijk wordt getoond, default 10.")
@click.option('--debug/--no-debug', default=False)
@click.option('--cuda/--no-cuda', default=True)
def search(folder: str, dataset: str, limit: int, debug: bool, cuda: bool) -> None:
    folder_path = os.path.abspath(os.curdir + "/" + folder)

    files = list((x for x in Path(folder_path).iterdir() if x.is_file()))
    errors = []

    cuda = use_cuda(cuda)
    init(cuda)

    print("⚡ Using CUDA!" if cuda else "🐢 CUDA not available, falling back to CPU processing!")

    if len(files) == 0:
        click.echo(f"Folder {folder} is empty!")
        return

    results = []

    with click.progressbar(files, show_pos=True, show_percent=True, label="Initializing...") as bar:
        for file in bar:
            file_name = str(file.resolve())
            img = cv2.imread(file_name)
            face_embeddings = get_face_embeddings(img, cuda)

            for face in face_embeddings:
                results += retrieve_data(face["face_embedding"], dataset)

            try:
                bar.label = f"Processing: {os.path.relpath(file)}"
            except Exception as error:
                bar.label = f"Error processing: {os.path.relpath(file)}"

                if debug:
                    errors.append(error)

                pass

    for error in errors:
        click.echo(error)

    if len(results) == 0:
        click.echo("No matches found")
        return

    print_results(results, file_name, limit)

    click.echo('Search finished!')


@cli.command(help="Geeft een lijst met alle beschikbare datasets")
def datasets() -> None:
    click.echo(retrieve_datasets())


@cli.command()
def setup() -> None:
    setup_db()
    click.echo(f'Done')


if __name__ == '__main__':
    cli()
