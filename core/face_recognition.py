import os
from typing import Optional
import dlib
import cv2
from core.DbConnection import DbConnection
from collections.abc import Callable
from psycopg2 import Error

facerec = None
shape_predictor: Optional[Callable] = None
face_detector: Optional[Callable] = None
use_cuda = False


def insert_data(dataset, file_name, face_emb, width, height, x, y):
    db = DbConnection()
    db_cursor = db.cursor
    db_cursor.execute(
        "INSERT INTO faces (dataset, file_name, face_embedding, width, height, x, y) VALUES (%s, %s, %s, %s, %s, point(%s, %s), point(%s, %s))",
        (dataset, file_name, face_emb, width, height, x[0], x[1], y[0], y[1]))


def init(cuda: bool) -> None:
    global facerec, shape_predictor, face_detector, use_cuda

    root_dir = os.path.abspath(os.path.dirname(__file__))
    face_rec_model_path = root_dir + '/data/dlib_face_recognition_resnet_model_v1.dat'
    predictor_path = root_dir + '/data/shape_predictor_68_face_landmarks.dat'
    detector_path = root_dir + '/data/mmod_human_face_detector.dat'

    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    shape_predictor = dlib.shape_predictor(predictor_path)
    use_cuda = dlib.DLIB_USE_CUDA and cuda

    face_detector = dlib.cnn_face_detection_model_v1(
        detector_path) if use_cuda else dlib.get_frontal_face_detector()


def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list


def process_file(dataset, file) -> bool:
    global use_cuda

    file_name = str(file.resolve())
    img = cv2.imread(file_name)

    if img is None:
        raise Exception("File not supported")

    height, width, _ = img.shape

    try:
        face_locations = face_detector(img, 1)
    except RuntimeError:
        raise Exception("Unable to detect face locations")

    for face in face_locations:
        rect = face.rect if use_cuda else face
        raw_shape = shape_predictor(img, rect)
        face_descriptor = facerec.compute_face_descriptor(img, raw_shape)
        face_emb = vec2list(face_descriptor)
        x = (rect.left(), rect.top())
        y = (rect.right(), rect.bottom())

        if len(face_emb) == 128:
            insert_data(dataset, file.name, face_emb, width, height, x, y)

    return True
