import click
import os
from math import ceil
from core.face_recognition import folder_enroll, folder_search, retrieve_datasets
from core.setup_db import setup_db
from cli.search_results import SearchResults, SearchResult

@click.group()
def cli():
    pass


@cli.command(help="Voegt een dataset toe aan de database en verwerkt alle gezichten hierin")
@click.argument('folder', type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False)
def enroll(folder: str, debug: bool) -> None:
    folder_path = os.path.abspath(folder)
    folder_enroll(folder, folder_path, debug)
    click.echo('Enrollment finished!')


@cli.command(help="Zoekt een gelijkend gezicht in de database van de meegegeven foto(s)")
@click.argument('folder', type=click.Path(exists=True))
@click.option("--dataset", "-d", "dataset", type=str, required=False, multiple=True, help="Kan meerdere keren gebruikt worden. De naam van een dataset waarin gezocht word. Als er geen dataset wordt aangegeven worden alle beschikbare datasets gebruikt.")
@click.option("--limit", "-l", "limit", type=int, required=False, default=10, help="Het maximaal aantal matches dat tegelijk wordt getoond, default 10.")
def search(folder: str, dataset: str, limit: int) -> None:
    path = os.path.abspath(folder)
    click.echo(f'Search: {dataset}')

    all_results = folder_search(path, dataset)
    
    for results in all_results:
        if all_results.index(results) > 0:
            click.confirm(f"Wil je de matches van het volgende bestand ({results[0]}) zien?", abort=True)

        class_results = []

        for result in results[1]:
            class_results.append(SearchResult(result[2], result[5], result[1]))

        results_table = SearchResults(results[0], class_results)
        results_size = len(results_table.results)

        for rows in range(ceil(results_size / limit)):
            continue_file = 'y'

            if rows > 0:
                continue_file = click.prompt(f"Matches {rows * limit} tot {min(rows * limit + limit, results_size)} van {results_size} zichtbaar. Will je de volgende {min(limit, results_size - rows * limit)} matches zien?", 
                                                default='y', show_default=False, type=click.Choice(['y', 'n']), show_choices=True)
            
            if continue_file == 'n':
                break

            results_table.print_results(rows * limit, limit)

@cli.command(help="Geeft een lijst met alle beschikbare datasets")
def list() -> None:
    click.echo(retrieve_datasets())

@cli.command()
def setup() -> None:
    setup_db()
    click.echo(f'Done')


@cli.command()
def test() -> None:
    click.echo(f'Test!')
