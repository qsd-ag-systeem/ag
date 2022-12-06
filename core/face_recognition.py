import os
from typing import Optional
import dlib
import cv2
from pathlib import Path
from core.DbConnection import DbConnection
from collections.abc import Callable

facerec = None
shape_predictor: Optional[Callable] = None
face_detector: Optional[Callable] = None
use_cuda = False


def insert_data(dataset, file_name, face_emb, width, height, x, y):
    try:
        db = DbConnection()
        db_cursor = db.cursor
        db_cursor.execute(
            "INSERT INTO faces (dataset, file_name, face_embedding, width, height, x, y) VALUES (%s, %s, %s, %s, %s, point(%s, %s), point(%s, %s))",
            (dataset, file_name, face_emb, width, height, x[0], x[1], y[0], y[1]))
    except:
        print("Insert error", dataset, file_name, width, height, x, y)

def retrieve_data(face_emb, datasets):
    try:
        db = DbConnection()
        db_cursor = db.cursor

        where_string = ""

        if (datasets != None and datasets != ()):
            where_string = """
                WHERE dataset IN ('{0}')
            """.format("','".join(datasets))
        

        query_string = """
            SELECT id, dataset, file_name, x, y,
                euclidian('{0}', face_embedding) AS eucl 
            FROM faces
            {1}
            ORDER BY eucl ASC
            """.format(face_emb, where_string).replace('[','{').replace(']','}')
        print(datasets)
        db_cursor.execute(query_string)
        result = db_cursor.fetchall()
        return result
    except Exception as e:
        print(f"Select error {face_emb} ", e)

def retrieve_datasets():
    try:
        db = DbConnection()
        db_cursor = db.cursor


        query_string = """
            SELECT DISTINCT dataset
            FROM faces
            """
        
        db_cursor.execute(query_string)
        result = db_cursor.fetchall()
        return result
    except Exception as e:
        print(f"Select error ", e)

def init():
    global facerec, shape_predictor, face_detector, use_cuda

    root_dir = os.path.abspath(os.path.dirname(__file__))
    face_rec_model_path = root_dir + '/data/dlib_face_recognition_resnet_model_v1.dat'
    predictor_path = root_dir + '/data/shape_predictor_68_face_landmarks.dat'
    detector_path = root_dir + '/data/mmod_human_face_detector.dat'

    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    shape_predictor = dlib.shape_predictor(predictor_path)
    use_cuda = dlib.DLIB_USE_CUDA

    if use_cuda:
        print("⚡ Using CUDA!")
        face_detector = dlib.cnn_face_detection_model_v1(detector_path)
    else:
        print("🐢 CUDA not available, falling back to CPU processing!")
        face_detector = dlib.get_frontal_face_detector()


def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list


def folder_enroll(dataset, path):
    detect_face_in_folder(path, dataset, 'enroll')

def folder_search(path, datasets):
    return detect_face_in_folder(path, datasets, 'search')

def detect_face_in_folder(path, dataset, command, debug = False):
    global use_cuda

    print("Initializing ...")
    init()
    files = (x for x in Path(path).iterdir() if x.is_file())

    result = []

    for file in files:
        file_name = str(file.resolve())
        print("Processing file", file_name, "...")

        try:
            img = cv2.imread(file_name)
            height, width, _ = img.shape
            face_locations = face_detector(img, 1)
            for (k, face) in enumerate(face_locations):
                try:
                    rect = face.rect if use_cuda else face
                    raw_shape = shape_predictor(img, rect)
                    face_descriptor = facerec.compute_face_descriptor(
                        img, raw_shape)
                    face_emb = vec2list(face_descriptor)

                    x = (rect.left(), rect.top())
                    y = (rect.right(), rect.bottom())

                    if len(face_emb) == 128:
                        if debug:
                            print("Processing", dataset,
                                    file_name, width, height, x, y)

                        if (command == 'enroll'):
                            insert_data(dataset, file.name, face_emb, width, height, x, y)

                        elif (command == 'search'):
                            result.append([
                                str(file.name),
                                retrieve_data(face_emb, dataset)
                                ])
                        
                except Exception as e:
                    print(f"Face processing error! {file_name} ", e)
        except Exception as e:
            print(f"Processing error! {file_name} ", e)

    if (command == 'search'):
        return result