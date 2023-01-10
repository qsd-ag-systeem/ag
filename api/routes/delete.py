from api.helpers.response import success_response, error_response
from flask import request
from core.delete import delete_dataset_by_name, delete_file_by_name, delete_dataset_file_by_name, \
    delete_dataset_files_by_name


def delete():
    data = request.get_json()
    if "dataset" not in data:
        return error_response("Dataset name is required")

    dataset = data["dataset"]

    if dataset == "":
        return error_response("Dataset name is required")

    file = ""
    remove_file: bool = False

    if "file" in data:
        file = data["file"]

    if "remove_file" in data:
        remove_file = data["remove_file"]

    if file != "":
        delete_file(dataset, file)
        if remove_file:
            for file_name in file:
                delete_dataset_file_by_name(dataset, file_name)
    else:
        delete_dataset(dataset)

        if remove_file:
            delete_dataset_files_by_name(dataset)

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
