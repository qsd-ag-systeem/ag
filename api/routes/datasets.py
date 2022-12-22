from flask import request
from werkzeug.exceptions import BadRequest
from core.search import retrieve_datasets, delete_dataset
from api.helpers.response import success_response, error_response


def get():
    try:
        datasets = retrieve_datasets()
        data = [{'name': ds[0], 'count': ds[1]} for ds in datasets]
        return success_response(data)
    except:
        return error_response('An error occurred while fetching the datasets')


# delete datasets here as well
def delete(dataset):
    try:
        data = request.get_json()
        delete_dataset(dataset, data.get('filename'), data.get('deleteFiles') or False)
        return success_response({"message": "Deletion was successful"})
    except BadRequest:
        delete_dataset(dataset)
        return success_response({"message": "Deletion was successful"})
    except Exception:
        return error_response('An error occurred during the deletion')
