import time

import click
from halo import Halo

from core.common import dataset_exists, print_table
from core.face_recognition import init, use_cuda
from core.search import retrieve_dataset_data, retrieve_knn_filtered_search_data, retrieve_msearch_knn_filtered_data


@click.command(help="Vergelijkt twee datasets en geeft de top resultaten weer.")
@click.option("--dataset1", "-d1", "dataset1", type=str, required=True, multiple=False)
@click.option("--dataset2", "-d2", "dataset2", type=str, required=True, multiple=False)
@click.option('--debug/--no-debug', default=False)
@click.option('--cuda/--no-cuda', default=True)
def cross_search(dataset1: str, dataset2: str, debug: bool, cuda: bool) -> None:
    """
    Search for similar faces in the database of the given image(s).
    """

    spinner = Halo(text=f"Cross searching dataset {dataset1} and {dataset2}", spinner='dots')
    spinner.start()

    # Checking if datasets exist
    for dataset in [dataset1, dataset2]:
        try:
            if not dataset_exists(dataset):
                spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
                click.echo(f"Dataset '{dataset}' does not exist.", err=True)
                exit(1)
        except Exception as e:
            spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
            click.echo(f"Dataset '{dataset}' does not exist.", err=True)
            exit(1)

    # Get all entries from dataset1
    spinner.text = f"Getting all entries from dataset {dataset1} ..."

    data = []
    try:
        data = list(retrieve_dataset_data(dataset1))
    except Exception as e:
        spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
        click.echo(f"An error occurred while retrieving data of dataset '{dataset}'.", err=True)
        click.echo(f"Error: {e}", err=True) if debug else None
        exit(1)

    # Get matching entries from dataset2
    spinner.text = f"Retrieving matching entries from dataset {dataset2} ..."

    results = []
    face_embeddings = [entry['_source']['face_embedding'] for entry in data]

    try:
        msearch_result = retrieve_msearch_knn_filtered_data(face_embeddings, (dataset2,), 1)

        for (key, result) in enumerate(msearch_result['responses']):
            if result['hits']['hits']:
                results.append({
                    'dataset1': data[key]['_source']['dataset'],
                    'dataset2': result['hits']['hits'][0]['_source']['dataset'],
                    'file1': data[key]['_source']['file_name'],
                    'file2': result['hits']['hits'][0]['_source']['file_name'],
                    'score': round(result['hits']['hits'][0]['_score'] * 100, 3),
                    'top_left_1': str(data[key]['_source']['top_left']),
                    'top_left_2': str(result['hits']['hits'][0]['_source']['top_left']),
                    'bottom_right1': str(data[key]['_source']['bottom_right']),
                    'bottom_right2': str(result['hits']['hits'][0]['_source']['bottom_right']),
                })

    except Exception as e:
        spinner.fail(f"Cross searching dataset {dataset1} and {dataset2} failed.")
        click.echo(f"An error occurred while retrieving data of dataset '{dataset}'.", err=True)
        click.echo(f"Error: {e}", err=True) if debug else None
        exit(1)

    spinner.succeed(f"Cross searching dataset {dataset1} and {dataset2} succeeded ({len(results)} matching face embeddings found).")

    # Sort results by score descending
    results = sorted(results, key=lambda k: k['score'], reverse=True)

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
