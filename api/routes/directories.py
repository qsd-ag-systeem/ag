from pathlib import Path
import os


def get_subdirs(dir: str = ""):
    cwd = os.getcwd()

    try:
        path_name = os.path.join(cwd, dir)
        p = Path(path_name)
        subdirs = [x for x in p.iterdir() if x.is_dir()]
        return [str(x.relative_to(cwd)) for x in subdirs]
    except Exception as e:
        print(e)
        return []

def directories(subpath = ""):
    subdirs = get_subdirs(subpath)
    return subdirs
