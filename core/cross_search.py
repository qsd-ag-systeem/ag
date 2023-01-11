from core.common import dataset_exists
from core.search import retrieve_dataset_data, retrieve_msearch_knn_filtered_data


def validate_datasets_get_first(dataset1, dataset2):
    # Checking if datasets exist
    for dataset in [dataset1, dataset2]:
        if not dataset_exists(dataset):
            raise Exception(f"Dataset '{dataset}' does not exist.")

        return list(retrieve_dataset_data(dataset1))


def cross_search_datasets(dataset1, dataset2):
    results = []
    data = validate_datasets_get_first(dataset1, dataset2)
    face_embeddings = [entry['_source']['face_embedding'] for entry in data]

    msearch_result = retrieve_msearch_knn_filtered_data(face_embeddings, (dataset2,), 1)

    for (key, result) in enumerate(msearch_result['responses']):
        if result['hits']['hits']:
            results.append({
                'dataset1': data[key]['_source']['dataset'],
                'dataset2': result['hits']['hits'][0]['_source']['dataset'],
                'file1': data[key]['_source']['file_name'],
                'file2': result['hits']['hits'][0]['_source']['file_name'],
                'score': round(result['hits']['hits'][0]['_score'] * 100, 3),
                'top_left_1': str(data[key]['_source']['top_left']),
                'top_left_2': str(result['hits']['hits'][0]['_source']['top_left']),
                'bottom_right1': str(data[key]['_source']['bottom_right']),
                'bottom_right2': str(result['hits']['hits'][0]['_source']['bottom_right']),
            })

    # Sort results by score descending
    return sorted(results, key=lambda k: k['score'], reverse=True)
