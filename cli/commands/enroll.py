import click
import os

from core.EsConnection import EsConnection
from core.common import get_files, refresh_index
from core.face_recognition import init, process_file, use_cuda


@click.command(help="Geef een folder met afbeeldingen aan die opgeslagen moeten worden in de database.")
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

    fail = 0
    success = 0
    with click.progressbar(files, show_pos=True, show_percent=True, label="Initializing...") as bar:
        for file in bar:
            try:
                process_errors = process_file(folder, file, cuda)

                if (process_errors):
                    errors.extend(process_errors)

                bar.label = f"Processing: {os.path.relpath(file)}"
                success += 1
            except Exception as error:
                bar.label = f"Error processing: {os.path.relpath(file)}"
                fail += 1

                if debug:
                    errors.append(error)

    # Refresh the index to make the documents available for search immediately
    refresh_index()

    for error in errors:
        click.echo(error)

    click.echo(f"Enrollment finished ({success} of {success + fail} enrolled)!")
