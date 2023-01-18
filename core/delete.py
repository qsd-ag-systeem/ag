import os
import shutil

from core.EsConnection import EsConnection
from core.common import dataset_exists, refresh_index


def delete_file_by_name(dataset: str, file_name: str):
    if not dataset_exists(dataset):
        raise Exception(f"Dataset '{dataset}' does not exist.")

    es = EsConnection()
    
    query = {
        "bool": {
            "must": [
                {
                    "term": {
                        "dataset": dataset,
                    },
                },
                {
                    "term": {
                        "file_name": file_name,
                    },
                }
            ]
        }
    }

    es.connection.delete_by_query(index=es.index_name, query=query)
    refresh_index()


def delete_dataset_by_name(dataset: str):
    if not dataset_exists(dataset):
        raise Exception(f"Dataset '{dataset}' does not exist.")

    es = EsConnection()
    query = {
        "term": {
            "dataset": dataset
        }
    }

    es.connection.delete_by_query(index=es.index_name, query=query)
    refresh_index()


def delete_dataset_files_by_name(dataset: str):
    folder_path = os.path.abspath(os.path.join(os.curdir, dataset))
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def delete_dataset_file_by_name(dataset: str, file_name: str):
    file_path = os.path.abspath(os.path.join(os.curdir, dataset, file_name))
    if os.path.exists(file_path):
        os.remove(file_path)
