from flask import request
from core.export_dataset import export_all, export_dataset

def export():
    data = request.get_json()
    if not "path" in data:
        return {
            "success": False,
            "message": "Export path is required"
        }
    
    export_path = data["path"]

    dataset = []
    errors = []

    if "dataset" in data:
        dataset = data["dataset"]

    try:    
        if dataset:
            export_dataset(export_path, dataset)
        else:
            export_all(export_path)
    except Exception as error:
        errors.append(str(error))

    return {
        "success": True,
        "errors": errors,
        "message": f"export finished to {export_path}"
    }
    