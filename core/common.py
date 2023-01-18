from pathlib import Path
from tabulate import tabulate
import os

from core.EsConnection import EsConnection

def get_files(abs_path: str):
    path = Path(abs_path)
    if path.is_dir():
        return list((x for x in path.iterdir() if x.is_file() and not x.name.startswith(".")))
    elif path.is_file() and not path.name.startswith("."):
        return [path]

def print_table(columns, values):
    print(tabulate(values, columns, tablefmt="grid"))

def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list

def env_is_ci():
    return (
        os.getenv("GITHUB_ACTIONS")
        or os.getenv("TRAVIS")
        or os.getenv("CIRCLECI")
        or os.getenv("GITLAB_CI")
    )

def dataset_exists(name: str) -> bool:
    es = EsConnection()

    try:
        result = es.connection.search(
            index=es.index_name,
            size=0,
            query={
                "term": {
                    "dataset": name
                }
            }
        )

        return result["hits"]["total"]["value"] > 0
    except:
        return False

def retrieve_datasets():
    es = EsConnection()

    result = es.connection.search(
        index=es.index_name,
        size=0,
        aggs={
            "all_datasets": {
                "terms": {
                    "field": "dataset"
                }
            },
            "dataset_count": {
                "cardinality": {
                    "field": "dataset"
                }
            }
        }
    )

    return result["aggregations"]["all_datasets"]["buckets"]

def refresh_index():
    es = EsConnection()
    es.connection.indices.refresh(index=es.index_name)

def delete_all_documents():
    es = EsConnection()
    es.connection.delete_by_query(index=es.index_name, query={"match_all": {}})
    refresh_index()