from flask import request
from core.export_dataset import export_all, export_dataset
from api.helpers.response import error_response, success_response

def export():
    data = request.get_json()
    if not "path" in data:
        return error_response("Export file path is required!")
    
    export_path = data["path"]

    dataset = []
    errors = []

    if "dataset" in data:
        dataset = data["dataset"]

    try:    
        if dataset:
            export_dataset(export_path, dataset)
        else:
            export_all(export_path)
    except Exception as error:
        errors.append(str(error))

    return success_response(errors=errors)
    