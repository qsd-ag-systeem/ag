import shutil
import os
import core.db as db
from core.model.face import Face
from sqlalchemy import func, text, column

import core.db as db

def retrieve_data(face_emb: list, datasets: tuple):
    session = db.Session()
    q = session.query(Face, column("eucl")).from_statement(text("SELECT id, dataset, file_name, x, y, euclidian(:points, face_embedding) AS eucl FROM faces WHERE dataset IN (:datasets) ORDER BY eucl ASC LIMIT 1000;")).params(points=str(face_emb).replace('[', '{').replace(']', '}'), datasets=datasets)
    result = q.all()
    return result


def retrieve_all_data(face_emb: list):
    session = db.Session()
    q = session.query(Face, column("eucl")).from_statement(text("SELECT id, dataset, file_name, x, y, euclidian(:points, face_embedding) AS eucl FROM faces ORDER BY eucl ASC LIMIT 1000;")).params(points=str(face_emb).replace('[', '{').replace(']', '}'))
    result = q.all()
    return result


def retrieve_datasets():
    session = db.Session()
    q = session.query(Face.dataset, func.count(Face.dataset)).group_by(Face.dataset)
    result = q.all()
    return result


def delete_dataset(dataset: str, delete_files: bool):
    session = db.Session()
    q = session.query(Face).filter(Face.dataset == dataset)
    result = q.all()
    if len(result) == 0:
        raise Exception("Dataset not found")

    if delete_files:
        folder_path = os.path.abspath(os.curdir + "/" + dataset)
        shutil.rmtree(folder_path)

    q.delete()
    session.commit()
    session.close()
