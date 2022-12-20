import csv
import os
from datetime import datetime
from math import ceil
import click
import cv2
from core.common import get_files, print_table
from core.face_recognition import init, use_cuda, search_file


@click.command(help="Zoekt een gelijkend gezicht in de database van de meegegeven foto(s).")
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
                results.extend(search_file(file, dataset, cuda))

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

                output_folder = os.path.abspath(
                    os.path.join(os.getcwd(), "output"))

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