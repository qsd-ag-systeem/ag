from flask import request
from core.export_dataset import export_datasets, export_datasets_by_name
from api.helpers.response import error_response, success_response


def export():
    data = request.get_json()
    if "path" not in data:
        return error_response("Export file path is required!")

    export_path = data["path"]

    dataset = []
    errors = []

    if "dataset" in data:
        dataset = data["dataset"]

    try:
        if dataset:
            export_datasets_by_name(export_path, dataset)
        else:
            export_datasets(export_path)
    except Exception as error:
        errors.append(str(error))

    return success_response(errors=errors)
