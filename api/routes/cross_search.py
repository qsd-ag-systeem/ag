from flask import request

from core.cross_search import cross_search_datasets
from core.import_dataset import import_all
from api.helpers.response import error_response, success_response


def cross_search():
    data = request.get_json()
    if "dataset1" not in data and "dataset2" not in data:
        return error_response("dataset1 and dataset2 are required fields")

    dataset1 = data["dataset1"]
    dataset2 = data["dataset2"]

    try:
        # Sort results by score descending
        data = sorted(cross_search_datasets(dataset1, dataset2), key=lambda k: k['score'], reverse=True)
        return success_response(data)
    except Exception as e:
        return error_response(str(e))

