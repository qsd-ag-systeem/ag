import click
from halo import Halo

from core.common import print_table
from core.cross_search import cross_search_datasets


@click.command(help="Vergelijkt twee datasets en geeft de top resultaten weer.")
@click.option("--dataset1", "-d1", "dataset1", type=str, required=True, multiple=False)
@click.option("--dataset2", "-d2", "dataset2", type=str, required=True, multiple=False)
@click.option('--debug/--no-debug', default=False)
@click.option('--cuda/--no-cuda', default=True)
def cross_search(dataset1: str, dataset2: str, debug: bool) -> None:
    """
    Search for similar faces in the database of the given image(s).
    """

    results = []
    spinner = Halo(text=f"Cross searching dataset {dataset1} and {dataset2}", spinner='dots')
    spinner.start()

    try:
        # Sort results by score descending
        results = sorted(cross_search_datasets(dataset1, dataset2), key=lambda k: k['score'], reverse=True)
    except Exception as e:
        spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
        click.echo(f"Error: {e}", err=True) if debug else None
        exit(1)

    spinner.succeed(f"Cross searching dataset {dataset1} and {dataset2} succeeded ({len(results)} matching face embeddings found).")

    # Print results in table
    columns = {
        'dataset1': "Dataset 1",
        'dataset2': "Dataset 2",
        'file1': "File 1",
        'file2': "Top match dataset 2",
        'score': "Score",
        'top_left_1': "Top left 1",
        'top_left_2': "Top left 2",
        'bottom_right1': "Bottom right 1",
        'bottom_right2': "Bottom right 2",
    }

    print_table(columns, results)

    exit(0)
