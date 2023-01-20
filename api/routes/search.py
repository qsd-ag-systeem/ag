import json
import os
import numpy as np
from flask import request
from core.face_recognition import init, search_file, use_cuda
from core.common import get_files
from api.helpers.response import error_response, success_response


def search():
    data = request.get_json()
    if "folder" not in data:
        return error_response("Folder or image is required")

    folder = data["folder"]
    cuda = data["cuda"] if "cuda" in data else False
    dataset = data["datasets"] if "datasets" in data else False
    folder_path = os.path.abspath(folder)

    if not os.path.exists(folder_path):
        return error_response(f"Folder or image \"{folder}\" does not exist!")

    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []
    result = []

    if len(files) == 0:
        return error_response(f"Folder or image \"{folder}\" is empty!")

    for file in files:
        try:
            search_results = search_file(
                file,
                dataset,
                cuda
            )

            for search_result in search_results:
                top_left = np.fromstring(
                    search_result[5].strip("[]"),
                    sep=', '
                )

                bottom_right = np.fromstring(
                    search_result[6].strip("[]"),
                    sep=', '
                )

                result.append({
                    "input_file": search_result[0],
                    "id": search_result[1],
                    "dataset": search_result[2],
                    "file_name": search_result[3],
                    "similarity": search_result[4],
                    "top_left": list(top_left),
                    "bottom_right": list(bottom_right),
                    "width": search_result[7],
                    "height": search_result[8],
                    "input": search_result[9],
                })

        except Exception as error:
            errors.append(str(error))
            pass

    results = sorted(result, key=lambda k: k['similarity'], reverse=True)

    return success_response(results, errors)
