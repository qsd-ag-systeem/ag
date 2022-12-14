"""
CLI for the face recognition application.
"""
from core.import_dataset import import_all
from core.export_dataset import export_all, export_dataset
from core.setup_db import setup_db
from core.search import delete_dataset, retrieve_all_data, retrieve_data, retrieve_datasets
from core.face_recognition import get_face_embeddings, init, process_file, use_cuda
from core.common import get_files, print_table
from slugify import slugify
import cv2
import click
from pathlib import Path
from math import ceil
from datetime import datetime
import os
import csv


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

    files = get_files(folder)

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
@click.option('--export', '-E', type=bool, default=False, is_flag=True, help="Exporteer de resultaten naar een csv bestand")
def search(folder: str, dataset: tuple, limit: int, debug: bool, cuda: bool, export: bool) -> None:
    """
    Search for similar faces in the database of the given image(s).
    """

    files = get_files(folder)

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

        results_size = len(results)

        if results_size == 0:
            click.echo("No matches found")
            return

        columns = ["Input file", "ID", "Dataset", "File name",
                   "Similarity (%)", "Left top", "Right bottom"]

        results = sorted(results, key=lambda x: x[4], reverse=True)

        if export:
            try:
                # Get todays date and time
                now = datetime.now()

                date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

                output_folder = Path(os.path.join(os.path.curdir, "output"))

                if not os.path.exists(output_folder):
                    os.mkdir(output_folder)

                file = f"{date_time}_search-results.csv"

                click.echo(
                    f"\nExporting results to {click.format_filename(file)}", nl=True)

                path = os.path.join(
                    output_folder, file)

                with open(path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(columns)
                    writer.writerows(results)
            except Exception as err:
                errors.append(err)
                click.echo(
                    "Something went wrong while exporting the results", err=True)
        else:
            # Sort results since it may contain results from multiple inputs

            for rows in range(ceil(results_size / limit)):
                continue_file = 'y'

                if rows > 0:
                    continue_file = click.prompt(
                        f"Resultaat {((rows - 1) * limit) + 1} t/m {min((rows - 1) * limit + limit, results_size)} van {results_size} worden weergegeven. Will je de volgende {min(limit, results_size - rows * limit)} matches zien?",
                        default='y', show_default=False, type=click.Choice(['y', 'n']), show_choices=True)

                if continue_file == 'n':
                    break

                print_table(
                    columns, results[rows * limit:rows * limit + limit])

    if debug:
        for error in errors:
            click.echo(error)


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


@cli.command()
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


@cli.command("import")
@click.argument('file_name', type=str)
def import_dataset(file_name: str) -> None:
    file_path = os.path.join(os.getcwd(), "input", f"{file_name}.csv")
    file = Path(file_path)

    if not file.is_file():
        click.echo(
            f"Error: a file with this name '{file_path}' doesn't exist.", err=True)
        return

    import_all(file_path)

    click.echo(f'Done')


if __name__ == '__main__':
    cli()
