from flask import request
from core.face_recognition import init, process_file, use_cuda
from core.common import get_files
from flask import current_app
import os
from api.helpers.response import error_response, success_response


def enroll():
    data = request.get_json()
    
    if "folder" not in data:
        return error_response("Folder is required")

    name = data["name"] if "name" in data else data["folder"]

    folder = data["folder"]
    cuda = data["cuda"] if "cuda" in data else False

    folder_path = os.path.abspath(os.curdir + "/" + folder)

    if not os.path.exists(folder_path):
        return error_response(f"Folder \"{folder}\" does not exist!")

    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []

    if len(files) == 0:
        return error_response(f"Folder {folder} is empty!")
    
    total = len(files)
    current = 0

    for file in files:
        success = True
        current += 1

        try:
            process_file(name, file, cuda)
        except Exception as error:
            errors.append(error)
            success = False
            pass
        
        socketio = current_app.extensions['socketio']
        socketio.emit('enroll', {
            "success": success,
            "current": current,
            "total": total,
            "file": file.name,
            "folder": folder
        })

    # it is a success response but could still contain errors
    return success_response(errors=errors)
