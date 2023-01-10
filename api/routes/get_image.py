import os
from flask import send_file


def get_image(path: str = ""):
    file_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return send_file(file_path)
