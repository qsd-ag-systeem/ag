import click
import os
import cv2
from math import ceil

from core.common import get_files, print_table
from core.search import retrieve_datasets, retrieve_data
from core.face_recognition import init, process_file, get_face_embeddings, use_cuda
from core.setup_db import setup_db


@click.group()
def cli():
    pass


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
@click.option('--cuda/--no-cuda', default=True)
def enroll(folder: str, debug: bool, cuda: bool) -> None:
    folder_path = os.path.abspath(os.curdir + "/" + folder)
    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []

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
@click.option("--dataset", "-d", "dataset", type=str, required=False, multiple=True,
              help="Kan meerdere keren gebruikt worden. De naam van een dataset waarin gezocht word. Als er geen dataset wordt aangegeven worden alle beschikbare datasets gebruikt.")
@click.option("--limit", "-l", "limit", type=int, required=False, default=10,
              help="Het maximaal aantal matches dat tegelijk wordt getoond, default 10.")
@click.option('--debug/--no-debug', default=False)
@click.option('--cuda/--no-cuda', default=True)
def search(folder: str, dataset: str, limit: int, debug: bool, cuda: bool) -> None:
    folder_path = os.path.abspath(os.curdir + "/" + folder)
    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []

    print("⚡ Using CUDA!" if cuda else "🐢 CUDA not available, falling back to CPU processing!")

    if len(files) == 0:
        click.echo(f"Folder {folder} is empty!")
        return

    results = []

    with click.progressbar(files, show_pos=True, show_percent=True, label="Initializing...") as bar:
        for file in bar:
            try:
                file_path = str(file.resolve())
                file_name = str(file.name)
                img = cv2.imread(file_path)
                face_embeddings = get_face_embeddings(img, cuda)

                for face in face_embeddings:
                    data = retrieve_data(face["face_embedding"], dataset)

                    for row in data:
                        results.append(
                            [file_name, row[0], row[1], row[2], round(100 - (row[5] * 100), 2), row[3], row[4]])

                bar.label = f"Processing: {os.path.relpath(file)}"
            except Exception as error:
                bar.label = f"Error processing: {os.path.relpath(file)}"

                if debug:
                    errors.append(error)

                pass

    for error in errors:
        click.echo(error)

    results_size = len(results)

    if results_size == 0:
        click.echo("No matches found")
        return

    # Sort results since it may contain results from multiple inputs
    results = sorted(results, key=lambda x: x[4], reverse=True)

    for rows in range(ceil(results_size / limit)):
        continue_file = 'y'

        if rows > 0:
            continue_file = click.prompt(
                f"Resultaat {((rows - 1) * limit) + 1} t/m {min((rows - 1) * limit + limit, results_size)} van {results_size} worden weergegeven. Will je de volgende {min(limit, results_size - rows * limit)} matches zien?",
                default='y', show_default=False, type=click.Choice(['y', 'n']), show_choices=True)

        if continue_file == 'n':
            break

        columns = ["Input file", "ID", "Dataset", "File name", "Similarity (%)", "Left top", "Right bottom"]
        print_table(columns, results[rows * limit:rows * limit + limit])


@cli.command(help="Geeft een lijst met alle beschikbare datasets")
def datasets() -> None:
    rows = retrieve_datasets()
    print_table(["Name", "Enrolled images"], rows)


@cli.command()
def setup() -> None:
    setup_db()
    click.echo(f'Done')


if __name__ == '__main__':
    cli()
