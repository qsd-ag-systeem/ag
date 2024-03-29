from api.helpers.response import success_response, error_response
from core.common import retrieve_datasets


def get():
    try:
        datasets = retrieve_datasets()
        data = [{
            'id': row["key"],
            'name': row["key"],
            'count': row["doc_count"]
        } for row in datasets]
        return success_response(data)
    except:
        return error_response('An error occurred while fetching the datasets')