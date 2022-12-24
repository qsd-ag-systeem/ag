import os
import shutil

from core.EsConnection import EsConnection
from core.common import dataset_exists


def delete_dataset_by_name(dataset: str):
    exists = dataset_exists(dataset)

    if not exists:
        raise Exception(f"Dataset '{dataset}' does not exist.")

    es = EsConnection()
    query = {
        "term": {
            "dataset": dataset
        }
    }

    es.connection.delete_by_query(index=es.index_name, query=query)


def delete_dataset_files_by_name(dataset: str):
    folder_path = os.path.abspath(os.path.join(os.curdir, dataset))
    shutil.rmtree(folder_path)
