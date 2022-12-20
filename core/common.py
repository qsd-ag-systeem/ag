from pathlib import Path
from tabulate import tabulate


def get_files(abs_path: str):
    path = Path(abs_path)
    if (path.is_dir()):
        return list((x for x in path.iterdir() if x.is_file() and not x.name.startswith(".")))
    elif (path.is_file() and not path.name.startswith(".")):
        return [path]

def print_table(columns, values):
    print(tabulate(values, columns, tablefmt="grid"))

def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list
