import os
from flask import send_file

from api.helpers.response import error_response


def get_image(path: str = ""):
    file_path = os.path.abspath(os.path.join(os.getcwd(), path))

    if not os.path.exists(file_path):
        return error_response(f"File '{path}' does not exist!")

    return send_file(file_path)
