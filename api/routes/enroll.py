from flask import request
from core.face_recognition import init, process_file, use_cuda
from core.common import get_files
from flask import current_app
import os


def enroll():
    data = request.get_json()
    if not "folder" in data:
        return {
            "success": False,
            "message": "Folder is required"
        }

    name = data["name"] if "name" in data else data["folder"]

    res = {}

    folder = data["folder"]
    cuda = data["cuda"] if "cuda" in data else False

    folder_path = os.path.abspath(os.curdir + "/" + folder)

    if not os.path.exists(folder_path):
        res["success"] = False
        res["message"] = f"Folder \"{folder}\" does not exist!"
        return res

    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []

    res["success"] = True

    if len(files) == 0:
        res["success"] = False
        res["message"] = f"Folder {folder} is empty!"
        return res
    
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
    
    res["message"] = "Enrollment finished"

    return res