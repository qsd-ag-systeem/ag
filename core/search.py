import elasticsearch.helpers
from core.EsConnection import EsConnection

def retrieve_dataset_data(dataset: str):
    es = EsConnection()

    results = elasticsearch.helpers.scan(
        es.connection,
        index=es.index_name,
        size=es.default_size,
        query={
            "query": {
                "term": {
                    "dataset": dataset
                }
            }
        }
    )

    return results


def retrieve_msearch_knn_filtered_data(face_emb: [list], datasets: tuple, limit: int = 100):
    es = EsConnection()

    body = []
    for emb in face_emb:
        body.append({
            "index": es.index_name
        })

        body.append({
            "size": es.default_size,
            "_source": {
                "excludes": [
                    "face_embedding"
                ]
            },
            "knn": {
                "field": "face_embedding",
                "query_vector": emb,
                "k": limit,
                "num_candidates": 100,
                "filter": {
                    "terms": {
                        "dataset": list(datasets)
                    }
                }
            }
        })

    result = es.connection.msearch(body=body)

    return result


def retrieve_knn_filtered_search_data(face_emb: list, datasets: tuple, limit: int = 100):
    es = EsConnection()

    result = es.connection.search(
        index=es.index_name,
        size=es.default_size,
        source_excludes=[
            "face_embedding"
        ],
        knn={
            "field": "face_embedding",
            "query_vector": face_emb,
            "k": limit,
            "num_candidates": 100,
            "filter": {
                "terms": {
                    "dataset": list(datasets)
                }
            }
        }
    )

    return result


def retrieve_knn_search_data(face_emb: list):
    es = EsConnection()

    result = es.connection.search(
        index=es.index_name,
        size=es.default_size,
        source_excludes=[
            "face_embedding"
        ],
        knn={
            "field": "face_embedding",
            "query_vector": face_emb,
            "k": es.default_size,
            "num_candidates": 100
        }
    )

    return result
