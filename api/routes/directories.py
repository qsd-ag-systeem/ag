from pathlib import Path
import os
from api.helpers.response import success_response, error_response


def get_subdirs(dir: str = ""):
    cwd = os.getcwd()

    try:
        path_name = os.path.join(cwd, dir)
        p = Path(path_name)
        subdirs = [x for x in p.iterdir() if x.is_dir()]
        return success_response([str(x.relative_to(cwd)) for x in subdirs])
    except Exception as e:
        print(e)
        return error_response()


def directories(subpath=""):
    return get_subdirs(subpath)
