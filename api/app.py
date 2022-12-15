from flask import Flask, request
from core.face_recognition import init, process_file, get_face_embeddings, use_cuda
from core.common import get_files
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {
        "message": "Hello, World!"
    }

@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()
    if not "folder" in data:
        return {
            "success": False,
            "message": "Folder is required"
        }
    
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

    for file in files:
        try:
            process_file(folder, file, cuda)
        except Exception as error:
            errors.append(error)
            pass

    res["errors"] = errors
    res["message"] = "Enrollment finished"

    return res


@app.errorhandler(404)
def page_not_found(e):
    return {
        "message": "Page not found"
    }, 404

def run():
    app.run(host='0.0.0.0', port=5000, debug=True)