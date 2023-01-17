import os

from flask import request
from flask_socketio import emit

from api.helpers.response import error_response, success_response
from core.common import get_files
from core.face_recognition import init, process_file, use_cuda

canceled = False

def cancel(data):
    global canceled
    canceled = True

def enroll(data):
    global canceled
    status = "idle"

    if "folder" not in data:
        emit("err", {
            "message": "Folder is required"
        })
        return

    folder = data["folder"]
    cuda = data["cuda"] if "cuda" in data else False

    folder_path = os.path.abspath(os.curdir + "/" + folder)

    if not os.path.exists(folder_path):
        emit("err", {
            "message": f"Folder \"{folder}\" does not exist!"
        })
        return

    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []

    totalFiles = len(files)

    if totalFiles == 0:
        emit("err", {
            "message": f"Folder {folder} is empty!"
        })
        return

    emit('enroll', {
        "dataset": folder,
        "success": False,
        "filesProcessed": 0,
        "totalFiles": totalFiles,
        "status":  status,
        "file": None,
        "folder": folder,
        "progress":0
    })

    for filesProcessed, file in enumerate(files):
        status = "processing"

        if canceled:
            emit("cancel", {
                "success": True
            })
            break

        success = True

        try:
            process_file(folder, file, cuda)
        except Exception as error:
            errors.append(error)
            success = False

        if totalFiles == filesProcessed + 1:
            status = "enrolled"

        emit('enroll', {
            "dataset": folder,
            "success": success,
            "filesProcessed": filesProcessed + 1,
            "totalFiles": totalFiles,
            "status":  status,
            "file": file.name,
            "folder": folder,
            "progress": (filesProcessed + 1) / totalFiles * 100
        })

    canceled = False
