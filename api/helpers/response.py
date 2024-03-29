from flask import make_response, jsonify, Response
from typing import Union


# any changes in this file should be discussed
def success_response(data = None, errors: list = None, status: int = 200) -> Response:
    body = {
        "data": data,
        "errors": errors or [],
    }

    return make_response(
        jsonify(body),
        status
    )


def error_response(errors: Union[list, str] = None, status: int = 400) -> Response:
    if isinstance(errors, str):
        errors = [errors]

    body = {
        "data": None,
        "errors": errors or [],
    }

    return make_response(
        jsonify(body),
        status
    )
