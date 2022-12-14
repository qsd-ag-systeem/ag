"""
CLI for the face recognition application.
"""

import os
from math import ceil

import click
import cv2

from core.common import get_files, print_table
from core.face_recognition import (get_face_embeddings, init, process_file,
                                   use_cuda)
from core.search import (delete_dataset, retrieve_all_data, retrieve_data,
                         retrieve_datasets)
from core.setup_db import setup_db


@click.group()
def cli():
    """
    CLI group for the face recognition application.
    """
    pass


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
@click.option('--cuda/--no-cuda', default=True)
def enroll(folder: str, debug: bool, cuda: bool) -> None:
    """
    Enroll the images from the given folder into the database.
    """
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
def search(folder: str, dataset: tuple, limit: int, debug: bool, cuda: bool) -> None:
    """
    Search for similar faces in the database of the given image(s).
    """
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
                # pylint: disable=E1101
                img = cv2.imread(file_path)
                face_embeddings = get_face_embeddings(img, cuda)

                for (key, face) in enumerate(face_embeddings):
                    try:
                        data = retrieve_data(face["face_embedding"], dataset) if dataset else retrieve_all_data(
                            face["face_embedding"])

                        for row in data:
                            results.append(
                                [file_name, row[0], row[1], row[2], round(100 - (row[5] * 100), 2), row[3], row[4]])
                    except Exception as err:
                        errors.append(
                            f"An error occurred while retrieving the data of face #{key + 1} in image {file_name}: {err}")

                bar.label = f"Processing: {os.path.relpath(file)}"
            except Exception as error:
                bar.label = f"Error processing: {os.path.relpath(file)}"
                errors.append(error)

                pass

    if debug:
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

        columns = ["Input file", "ID", "Dataset", "File name",
                   "Similarity (%)", "Left top", "Right bottom"]
        print_table(columns, results[rows * limit:rows * limit + limit])


@cli.command(help="Geeft een lijst met alle beschikbare datasets")
@click.option('--debug/--no-debug', default=False)
def datasets(debug: bool) -> None:
    """
    This command lists all available datasets.
    """
    try:
        rows = retrieve_datasets()
        print_table(["Name", "Enrolled images"], rows)
    except Exception as err:
        error = f": {err}" if debug else ""
        click.echo(
            f"An error occurred while fetching the datasets{error}", err=True)


@cli.command(help="Verwijdert een dataset")
@click.argument('dataset', type=str)
@click.option('--debug/--no-debug', default=False)
@click.option('--delete-files/--no-delete-files', default=False)
def delete(dataset: str, debug: bool, delete_files: bool) -> None:
    """
    This command deletes a dataset.
    """
    try:
        delete_dataset(dataset, delete_files)
        click.echo(f"Dataset \"{dataset}\" removed successfully")
    except Exception as err:
        error = f": {err}" if debug else ""
        click.echo(
            f"An error occurred while deleting the dataset{error}", err=True)


@cli.command()
def setup() -> None:
    """
    This command sets up the database.
    """
    setup_db()
    click.echo('Done')


if __name__ == '__main__':
    cli()
