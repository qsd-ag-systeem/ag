import click
import os
from math import ceil
from core.face_recognition import folder_enroll, folder_search, retrieve_datasets
from core.setup_db import setup_db
from cli.search_results import SearchResults, SearchResult


@click.group()
def cli():
    pass


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
def enroll(folder: str, debug: bool) -> None:
    folder_path = os.path.abspath(folder)
    folder_enroll(folder, folder_path, debug)
    click.echo('Enrollment finished!')


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option("--dataset", "-d", "dataset", type=str, required=False, multiple=True, help="De naam van een bestaande dataset. In het geval dat bij de enrollment een naam is gekozen anders dan de folder naam kan ook de folder naam alsnog gebruikt worden bij het verwijderen.")
@click.option("--limit", "-l", "limit", type=int, required=False, default=10, help="Het maximaal aantal matches dat tegelijk wordt getoond, standaard 10")
def search(folder: str, dataset: str, limit: int) -> None:
    path = os.path.abspath(folder)
    click.echo(f'Search: {dataset}')

    all_results = folder_search(path, dataset)
    
    for results in all_results:
        class_results = []

        for result in results[1]:
            class_results.append(SearchResult(result[2], result[5], result[1]))

        results_table = SearchResults(results[0], class_results)
        results_size = len(results_table.results)

        for rows in range(ceil(results_size / limit)):
            if rows > 0:
                click.confirm(f"Matches {rows * limit} tot {min(rows * limit + limit, results_size)} van {results_size} zichtbaar. Will je de volgende {min(limit, results_size - rows * limit)} matches zien?", abort=True)
            results_table.print_results(rows * limit, limit)

@cli.command()
def list() -> None:
    click.echo(retrieve_datasets())

@cli.command()
def setup() -> None:
    setup_db()
    click.echo(f'Done')


@cli.command()
def test() -> None:
    click.echo(f'Test!')
