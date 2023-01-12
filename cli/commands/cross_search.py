import click
from halo import Halo

from core.cross_search import get_sorted_results, validate_datasets_get_first, get_msearch_data, get_face_embeddings_from_data
from core.common import print_table


@click.command(help="Vergelijkt twee datasets en geeft de top resultaten weer.")
@click.option("--dataset1", "-d1", "dataset1", type=str, required=True, multiple=False)
@click.option("--dataset2", "-d2", "dataset2", type=str, required=True, multiple=False)
@click.option('--debug/--no-debug', default=False)
def cross_search(dataset1: str, dataset2: str, debug: bool) -> None:
    """
    Search for similar faces in the database of the given image(s).
    """

    data = []
    results = []
    msearch_result = []
    face_embeddings = []

    spinner = Halo(text=f"Cross searching dataset {dataset1} and {dataset2}", spinner='dots')
    spinner.start()

    spinner.text = f"Retrieving all entries from dataset {dataset1} ..."

    try:
        data = validate_datasets_get_first(dataset1, dataset2)
    except Exception as e:
        spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
        click.echo(f"Error: {e}", err=True) if debug else None
        exit(1)

    # Get matching entries from dataset2
    spinner.text = f"Retrieving matching entries from dataset {dataset2} ..."

    try:
        face_embeddings = get_face_embeddings_from_data(data)
    except Exception as e:
        spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
        click.echo(f"Error: {e}", err=True) if debug else None
        exit(1)

    if len(face_embeddings) > 5000:
        spinner.warn(f"Dataset {dataset1} contains more than 5000 entries. This may take a while, please be patient.")
        spinner.start()

    spinner.text = f"Retrieving matching entries from dataset {dataset2} ..."

    try:
        msearch_result = get_msearch_data(face_embeddings, dataset2)
    except Exception as e:
        spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
        click.echo(f"Error: {e}", err=True) if debug else None
        exit(1)

    # Sort results by score descending
    spinner.text = f"Processing results ..."

    try:
        results = get_sorted_results(data, msearch_result)
    except Exception as e:
        spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
        click.echo(f"Error: {e}", err=True) if debug else None
        exit(1)

    spinner.succeed(
        f"Cross searching dataset {dataset1} and {dataset2} succeeded ({len(results)} matching face embeddings found).")

    # Print results in table
    columns = {
        'dataset1': "Dataset 1",
        'dataset2': "Dataset 2",
        'file1': "File 1",
        'file2': "Top match dataset 2",
        'score': "Score",
        'top_left_1': "Top left 1",
        'top_left_2': "Top left 2",
        'bottom_right_1': "Bottom right 1",
        'bottom_right_2': "Bottom right 2",
    }

    # Print the first 100 results
    print_table(columns, results)

    exit(0)
