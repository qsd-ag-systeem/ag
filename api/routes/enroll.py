import os

from flask import request
from flask_socketio import emit

from api.helpers.response import error_response, success_response
from core.common import get_files
from core.face_recognition import init, process_file, use_cuda


canceled = False;

def cancel(data):
    global canceled

    canceled = True



def enroll(data):
    global canceled
    status = "idle"

    if "folder" not in data:
        pass
        # return error_response("Folder is required")


    folder = data["folder"]
    cuda = data["cuda"] if "cuda" in data else False
    name = data["name"] if "name" in data else folder

    folder_path = os.path.abspath(os.curdir + "/" + folder)

    if not os.path.exists(folder_path):
        pass
        # return error_response(f"Folder \"{folder}\" does not exist!")

    files = get_files(folder_path)

    cuda = use_cuda(cuda)
    init(cuda)

    errors = []

    if len(files) == 0:
        pass
        # return error_response(f"Folder {folder} is empty!")
    totalFiles = len(files)

    emit('enroll', {
        "dataset": name,
        "success": False,
        "filesProcessed": 0,
        "totalFiles": totalFiles,
        "status":  status,
        "file": None,
        "folder": folder,
        "progress":0
    })


    # socketio = current_app.extensions['socketio']

    # def cancel(data):
    #     nonlocal canceled
    #     if data["folder"] == folder:
    #         canceled = True

    # socketio.on_event('cancel', cancel)

    for filesProcessed, file in enumerate(files):
        status = "processing"


        if canceled:
            # emit("cancel")
            break
        # if canceled:
        #     return error_response("Canceled")

        success = True
        try:
            process_file(name, file, cuda)
        except Exception as error:
            errors.append(error)
            success = False
            pass

        if totalFiles == filesProcessed + 1:
            status = "enrolled"


        emit('enroll', {
            "dataset": name,
            "success": success,
            "filesProcessed": filesProcessed + 1,
            "totalFiles": totalFiles,
            "status":  status,
            "file": file.name,
            "folder": folder,
            "progress": (filesProcessed + 1) / totalFiles * 100
        })

    canceled = False
    # it is a success response but could still contain errors
    # return success_response(errors=errors)
