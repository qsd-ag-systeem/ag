import os
from pathlib import Path
from tabulate import tabulate


def get_abs_path_from_rel_folder(folder: str = ""):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", folder))

def get_files(abs_path: str):
    return list((x for x in Path(abs_path).iterdir() if x.is_file() and not x.name.startswith(".")))


def print_table(columns, values):
    print(tabulate(values, columns, tablefmt="grid"))


def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list
