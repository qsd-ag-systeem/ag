import os
from flask import request
from core.face_recognition import init, search_file, use_cuda
from core.common import get_files


def search():
    data = request.get_json()
    if not "folder" in data:
        return {
            "success": False,
            "message": "Folder or image is required"
        }

    res = {}
    folder = data["folder"]
    cuda = data["cuda"] if "cuda" in data else False
    dataset = data["dataset"] if "dataset" in data else False
    folder_path = os.path.abspath(folder)

    if not os.path.exists(folder_path):
        res["success"] = False
        res["message"] = f"Folder or image \"{folder}\" does not exist!"
        return res

    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []
    result = []
    
    res["success"] = True

    if len(files) == 0:
        res["success"] = False
        res["message"] = f"Folder or image \"{folder}\" is empty!"
        return res
    
    for file in files:
        try:
            result.extend(search_file(file, dataset, cuda))
        except Exception as error:
            errors.append(error)
            pass

    res["result"] = result
    res["errors"] = errors
    res["message"] = "Search finished"

    return res