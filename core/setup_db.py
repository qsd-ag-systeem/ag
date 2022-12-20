import os
from core.DbConnection import DbConnection
from core.EsConnection import EsConnection


def setup_db():
    setup_es()
    return

    root_dir = os.path.abspath(os.curdir)

    db = DbConnection()
    db.cursor.execute(open(root_dir + "/core/sql/setup_db.sql", "r").read())
    db.cursor.execute(open(root_dir + "/core/sql/vec_sub_func.sql", "r").read())
    db.cursor.execute(open(root_dir + "/core/sql/euclidian_func.sql", "r").read())


def setup_es():
    es = EsConnection()

    mapping = {
        "mappings": {
            "properties": {
                "dataset": {"type": "keyword"},
                "file_name": {"type": "keyword"},
                "width": {"type": "keyword"},
                "height": {"type": "keyword"},
                "pos_top": {"type": "keyword"},
                "pos_left": {"type": "keyword"},
                "pos_right": {"type": "keyword"},
                "pos_bottom": {"type": "keyword"},
                "face_embedding":{
                    "type": "dense_vector",
                    "dims": 128
                },
            }
        }
    }

    es.connection.indices.create(index="face_recognition", body=mapping)
