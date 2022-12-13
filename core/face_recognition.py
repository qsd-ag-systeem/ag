import os
from typing import Optional
import dlib
import cv2
from collections.abc import Callable
from psycopg2 import Error
import core.db as db
from core.model.face import Face
from core.common import vec2list

facerec = None
shape_predictor: Optional[Callable] = None
face_detector: Optional[Callable] = None


def use_cuda(enable_cuda: bool = False) -> bool:
    return dlib.DLIB_USE_CUDA and enable_cuda


def insert_data(dataset, file_name, face_emb, width, height, x, y):
    session = db.Session()
    face = Face(dataset, file_name, width, height, x, y, face_emb)
    session.add(face)
    session.commit()
    session.close()

def init(cuda: bool) -> None:
    global facerec, shape_predictor, face_detector


    root_dir = os.path.abspath(os.path.dirname(__file__))
    face_rec_model_path = root_dir + '/data/dlib_face_recognition_resnet_model_v1.dat'
    predictor_path = root_dir + '/data/shape_predictor_68_face_landmarks.dat'
    detector_path = root_dir + '/data/mmod_human_face_detector.dat'

    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    shape_predictor = dlib.shape_predictor(predictor_path)

    face_detector = dlib.cnn_face_detection_model_v1(detector_path) if cuda else dlib.get_frontal_face_detector()


def process_file(dataset, file, cuda: bool = False) -> bool:
    file_name = str(file.resolve())
    img = cv2.imread(file_name)
    face_embeddings = get_face_embeddings(img, cuda)

    for face_emb in face_embeddings:
        insert_data(dataset, file.name, face_emb["face_embedding"], face_emb["width"], face_emb["height"], face_emb["x"], face_emb["y"])

    return True


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
            face_embeddings.append({"face_embedding": face_emb, "width": width, "height": height, "x": x, "y": y})

    return face_embeddings
