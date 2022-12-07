import click

from core.DbConnection import DbConnection
from math import ceil
from cli.search_results import SearchResults, SearchResult


def retrieve_data(face_emb, datasets):
    try:
        db = DbConnection()
        db_cursor = db.cursor

        where_string = ""

        if (datasets != None and datasets != ()):
            where_string = """
                WHERE dataset IN ('{0}')
            """.format("','".join(datasets))

        query_string = """
            SELECT id, dataset, file_name, x, y,
                euclidian('{0}', face_embedding) AS eucl 
            FROM faces
            {1}
            ORDER BY eucl ASC
            """.format(face_emb, where_string).replace('[', '{').replace(']', '}')
        db_cursor.execute(query_string)
        result = db_cursor.fetchall()
        return result
    except Exception as e:
        print(f"Select error {face_emb} ", e)


def retrieve_datasets():
    try:
        db = DbConnection()
        db_cursor = db.cursor

        query_string = """
            SELECT DISTINCT dataset
            FROM faces
            """

        db_cursor.execute(query_string)
        result = db_cursor.fetchall()
        return result
    except Exception as e:
        print(f"Select error ", e)


def print_results(results, name, limit):
    class_results = []

    for result in results:
        class_results.append(SearchResult(result[2], result[5], result[1]))

    results_table = SearchResults(name, class_results)
    results_size = len(results_table.results)

    for rows in range(ceil(results_size / limit)):
        continue_file = 'y'

        if rows > 0:
            continue_file = click.prompt(
                f"Matches {rows * limit} tot {min(rows * limit + limit, results_size)} van {results_size} zichtbaar. Will je de volgende {min(limit, results_size - rows * limit)} matches zien?",
                default='y', show_default=False, type=click.Choice(['y', 'n']), show_choices=True)

        if continue_file == 'n':
            break

        results_table.print_results(rows * limit, limit)