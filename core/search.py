import shutil
import os
import core.db as db
from core.model.face import Face
from sqlalchemy import func, text, column


def retrieve_data(face_emb: list, datasets: tuple):
    session = db.Session()
    points = str(face_emb).replace('[', '{').replace(']', '}')
    query = "SELECT id, dataset, file_name, x, y, euclidian(:points, face_embedding) AS eucl FROM faces " \
            "WHERE dataset IN (:datasets) ORDER BY eucl ASC LIMIT 1000;"

    q = session.query(Face, column("eucl")).from_statement(text(query)).params(points=points, datasets=datasets)
    result = q.all()
    return result


def retrieve_all_data(face_emb: list):
    session = db.Session()
    points = str(face_emb).replace('[', '{').replace(']', '}')
    query = "SELECT id, dataset, file_name, x, y, euclidian(:points, face_embedding) AS eucl FROM faces " \
            "ORDER BY eucl ASC LIMIT 1000;"

    q = session.query(Face, column("eucl")).from_statement(text(query)).params(points=points)
    result = q.all()
    return result


def retrieve_datasets():
    session = db.Session()
    q = session.query(Face.dataset, func.count(Face.dataset)).group_by(Face.dataset)
    result = q.all()
    return result


def delete_dataset(dataset: str, file: str = None, delete_files: bool = False):
    session = db.Session()
    # big ugly but hopefully we will move to elastic search
    if file:
        q = session.query(Face).filter(Face.dataset == dataset, Face.file_name == file)
    else:
        q = session.query(Face).filter(Face.dataset == dataset)
    result = q.all()

    if len(result) == 0:
        raise Exception("Dataset or file not found")

    if delete_files:
        file_path = '/' + file if file else ''
        folder_path = os.path.abspath(os.curdir + "/" + dataset + file_path)
        os.remove(folder_path) if file else shutil.rmtree(folder_path)

    q.delete()
    session.commit()
    session.close()
