import os
from core.DbConnection import DbConnection


def setup_db():
    root_dir = os.path.abspath(os.curdir)

    db = DbConnection()
    db.cursor.execute(open(root_dir + "/core/sql/setup_db.sql", "r").read())
    db.cursor.execute(open(root_dir + "/core/sql/vec_sub_func.sql", "r").read())
    db.cursor.execute(open(root_dir + "/core/sql/euclidian_func.sql", "r").read())
