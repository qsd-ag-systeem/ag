from core.EsConnection import EsConnection


def retrieve_data(face_emb: list, datasets: tuple):
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
            "k": 100,
            "num_candidates": 100,
            "filter": {
                "terms": {
                    "dataset": list(datasets)
                }
            }
        }
    )

    return result


def retrieve_all_data(face_emb: list):
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
