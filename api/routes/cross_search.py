from flask import request

from core.cross_search import get_cross_search_data
from api.helpers.response import error_response, success_response


def cross_search():
    data = request.get_json()
    if "dataset1" not in data and "dataset2" not in data:
        return error_response("dataset1 and dataset2 are required fields")

    dataset1 = data["dataset1"]
    dataset2 = data["dataset2"]

    try:
        # Sort results by score descending
        data = get_cross_search_data(dataset1, dataset2)
        return success_response(data)
    except Exception as e:
        return error_response(str(e))

