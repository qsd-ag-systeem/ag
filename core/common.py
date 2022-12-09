from pathlib import Path
from tabulate import tabulate


def get_files(abs_path):
    return list((x for x in Path(abs_path).iterdir() if x.is_file() and not x.name.startswith(".")))


def print_table(columns, values):
    print(tabulate(values, columns, tablefmt="grid"))


def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list
