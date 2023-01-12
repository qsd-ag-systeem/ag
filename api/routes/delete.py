from api.helpers.response import success_response, error_response
from flask import request

from api.schemas.delete_dataset import DeleteDatasetInput
from core.common import dataset_exists
from core.delete import delete_dataset_by_name, delete_file_by_name, delete_dataset_file_by_name, \
    delete_dataset_files_by_name


def delete():
    inputs = DeleteDatasetInput(request)
    if not inputs.validate():
        return error_response(inputs.errors)

    dataset = request.json.get('dataset')

    if not dataset_exists(dataset):
        return error_response(f"Dataset {dataset} does not exist")

    remove_file = request.json.get('remove_file')

    files = []
    if "files" in request.json:
        files = request.json.get('files')

    if len(files) > 0:
        delete_file(dataset, files)

        if remove_file:
            for file_name in files:
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
