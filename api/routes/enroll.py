from flask import request
from core.face_recognition import init, process_file, use_cuda
from core.common import get_files
import os
from api.helpers.response import error_response


def enroll():
    data = request.get_json()
    if "folder" not in data:
        return error_response(["Folder is required"])

    folder = data["folder"]
    cuda = data["cuda"] if "cuda" in data else False

    folder_path = os.path.abspath(os.curdir + "/" + folder)

    if not os.path.exists(folder_path):
        return error_response([f"Folder \"{folder}\" does not exist!"])

    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []

    if len(files) == 0:
        return error_response([f"Folder {folder} is empty!"])

    for file in files:
        try:
            process_file(folder, file, cuda)
        except Exception as error:
            errors.append(error)
            pass

    # it is a success response but could still contain errors
    return error_response(errors, 200)
