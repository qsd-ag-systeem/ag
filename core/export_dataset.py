import csv
from elasticsearch.exceptions import NotFoundError, RequestError

from core.EsConnection import EsConnection


def export_datasets(file):
    es = EsConnection()

    documents = []
    response = es.connection.options(
        request_timeout=5000,
    ).search(
        index=es.index_name,
        size=10000,
        scroll=es.default_scroll_time
    )

    while len(response['hits']['hits']):
        documents.extend(response['hits']['hits'])
        response = es.connection.scroll(scroll_id=response['_scroll_id'], scroll=es.default_scroll_time)

    write_es_export_to_file(file, documents)


def export_datasets_by_name(file, datasets: tuple):
    es = EsConnection()

    query = {
        "terms": {
            "dataset": list(datasets)
        }
    }

    documents = []
    response = es.connection.options(
        request_timeout=es.default_timeout,
    ).search(
        index=es.index_name,
        query=query,
        size=10000,
        scroll=es.default_scroll_time
    )

    while len(response['hits']['hits']):
        documents.extend(response['hits']['hits'])
        response = es.connection.scroll(scroll_id=response['_scroll_id'], scroll=es.default_scroll_time)

    write_es_export_to_file(file, documents)


def write_es_export_to_file(file, rows):
    if len(list(rows)) == 0:
        raise Exception("No data found.")

    es = EsConnection()

    mapping = es.connection.indices.get_mapping(index=es.index_name)
    mapping = mapping[es.index_name]['mappings']['properties'].keys()

    with open(file, 'w') as f:
        w = csv.DictWriter(f, mapping, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        w.writeheader()

        try:
            w.writerows((document['_source'] for document in rows))
        except (NotFoundError, RequestError):
            pass
