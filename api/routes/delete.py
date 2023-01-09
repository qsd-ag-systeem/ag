from api.helpers.response import success_response, error_response
from flask import request
from core.delete import delete_dataset_by_name, delete_file_by_name

def delete():
    data = request.get_json()
    if "dataset" not in data:
        return error_response("Dataset name is required")

    dataset = data["dataset"]
    file = ""

    if "file" in data:
        file = data["file"]

    if(file != ""):
        delete_file(dataset, file)
    else:
        delete_dataset(dataset)
    
    return success_response()

def delete_file(dataset, files):
    try:
        for file in files:
            delete_file_by_name(dataset, file)

    except Exception as e:
        return error_response()


def delete_dataset(dataset):
    try:
        delete_dataset_by_name(dataset)

    except Exception as e:
        return error_response()