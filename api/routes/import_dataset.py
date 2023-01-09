from flask import request
from core.import_dataset import import_all
from api.helpers.response import error_response, success_response

def import_dataset():
    data = request.get_json()
    if "path" not in data:
        return error_response("Import file path is required!")

    import_path = data["path"]

    errors = []

    try:
        import_all(import_path)
    except Exception as error:
        errors.append(str(error))

    return success_response(errors=errors)