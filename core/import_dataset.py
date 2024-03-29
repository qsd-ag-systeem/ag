import csv
import numpy as np
from elasticsearch import helpers
import multiprocessing

from core.EsConnection import EsConnection
from core.common import refresh_index


def customize(generator):
    for row in generator:
        row['bottom_right'] = np.fromstring(
            row['bottom_right'].strip("[]"), sep=', ')
        row['top_left'] = np.fromstring(row['top_left'].strip("[]"), sep=', ')
        row['face_embedding'] = np.fromstring(
            row['face_embedding'].strip("[]"), sep=', ')
        yield row


def import_all(file):
    es = EsConnection()

    with open(file) as f:
        reader = customize(csv.DictReader(f))

        action_list = []
        for (key, row) in enumerate(reader):
            record = {
                '_op_type': 'update',
                '_index': es.index_name,
                '_id': f"{row['dataset']}/{row['file_name']}-{key}",
                'doc': row,
                "doc_as_upsert": True
            }

            action_list.append(record)

        threads = int(multiprocessing.cpu_count() * 0.75)
        for success, info in helpers.parallel_bulk(es.connection, action_list, request_timeout=es.default_timeout, thread_count=threads, chunk_size=10000):
            if not success:
                print("Insert failed: ", info)

    # Refresh the index to make the documents available for search immediately
    refresh_index()
