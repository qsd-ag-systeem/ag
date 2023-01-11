import os
from typing import Optional
import dlib
import cv2
from collections.abc import Callable

from core.EsConnection import EsConnection
from core.common import vec2list
from core.search import retrieve_knn_search_data, retrieve_knn_filtered_search_data

facerec = None
shape_predictor: Optional[Callable] = None
face_detector: Optional[Callable] = None


def use_cuda(enable_cuda: bool = False) -> bool:
    return dlib.DLIB_USE_CUDA and enable_cuda


def insert_data(dataset, file_name, face_emb, width, height, x, y, key=0):
    es = EsConnection()

    doc_id = f"{dataset}/{file_name}-{key}"
    doc = {
        "dataset": dataset,
        "file_name": file_name,
        "width": width,
        "height": height,
        "top_left": x,
        "bottom_right": y,
        "face_embedding": face_emb,
    }
    es.connection.update(index=es.index_name, id=doc_id, doc=doc, doc_as_upsert=True)


def init(cuda: bool) -> None:
    global facerec, shape_predictor, face_detector

    root_dir = os.path.abspath(os.path.dirname(__file__))
    face_rec_model_path = root_dir + '/data/dlib_face_recognition_resnet_model_v1.dat'
    predictor_path = root_dir + '/data/shape_predictor_68_face_landmarks.dat'
    detector_path = root_dir + '/data/mmod_human_face_detector.dat'

    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    shape_predictor = dlib.shape_predictor(predictor_path)

    face_detector = dlib.cnn_face_detection_model_v1(
        detector_path) if cuda else dlib.get_frontal_face_detector()


def process_file(dataset, file, cuda: bool = False) -> bool:
    file_name = str(file.resolve())
    img = cv2.imread(file_name)
    face_embeddings = get_face_embeddings(img, cuda)

    for (key, face_emb) in enumerate(face_embeddings):
        insert_data(
            dataset,
            file.name,
            face_emb["face_embedding"],
            face_emb["width"],
            face_emb["height"],
            face_emb["x"],
            face_emb["y"],
            key
        )

    return True


def search_file(file, dataset, cuda=False):
    results = []
    file_path = str(file.resolve())
    file_name = str(file.name)
    img = cv2.imread(file_path)
    face_embeddings = get_face_embeddings(img, cuda)

    for (key, face) in enumerate(face_embeddings):
        try:
            if dataset:
                data = retrieve_knn_filtered_search_data(face["face_embedding"], dataset)
            else:
                data = retrieve_knn_search_data(face["face_embedding"])

            for row in data["hits"]["hits"]:
                results.append([
                    file_name,
                    row["_id"],
                    row["_source"]["dataset"],
                    row["_source"]["file_name"],
                    round(row["_score"] * 100, 3),
                    str(row["_source"]["top_left"]),
                    str(row["_source"]["bottom_right"]),
                ])
        except:
            pass

    return results


def get_face_embeddings(img, cuda: bool):
    face_embeddings = []

    if img is None:
        raise Exception("File not supported")

    height, width, _ = img.shape

    try:
        face_locations = face_detector(img, 1)
    except RuntimeError:
        raise Exception("Unable to detect face locations")

    for face in face_locations:
        rect = face.rect if cuda else face
        raw_shape = shape_predictor(img, rect)
        face_descriptor = facerec.compute_face_descriptor(img, raw_shape)
        face_emb = vec2list(face_descriptor)
        x = (rect.left(), rect.top())
        y = (rect.right(), rect.bottom())

        if len(face_emb) == 128:
            face_embeddings.append({
                "face_embedding": face_emb,
                "width": width,
                "height": height,
                "x": x,
                "y": y
            })

    return face_embeddings
