from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

delete_dataset_schema = {
    "type": "object",
    "properties": {
        "dataset": {"type": "string"},
        "files": {"type": "array", "items": {"type": "string"}},
        "remove_file": {"type": "boolean"}
    },
    "required": ["dataset", "remove_file"],
}

class DeleteDatasetInput(Inputs):
    json = [JsonSchema(schema=delete_dataset_schema)]
