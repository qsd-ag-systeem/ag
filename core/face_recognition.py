import os
import dlib
import cv2
from pathlib import Path
from core.DbConnection import DbConnection

facerec = None
shape_predictor = None
face_detector = None
use_cuda = False


def insert_data(dataset, file_name, face_emb):
    print("insert", dataset, file_name)
    db = DbConnection()
    db_cursor = db.cursor
    db_cursor.execute("INSERT INTO faces (dataset, file_name, face_embedding) VALUES (%s, %s, %s)",
                      (dataset, file_name, face_emb))


def init():
    global facerec, shape_predictor, face_detector, use_cuda

    root_dir = os.path.abspath(os.curdir)
    face_rec_model_path = root_dir + '/core/data/dlib_face_recognition_resnet_model_v1.dat'
    predictor_path = root_dir + '/core/data/shape_predictor_68_face_landmarks.dat'
    detector_path = root_dir + '/core/data/mmod_human_face_detector.dat'

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


def folder_exec(dataset, path):
    global use_cuda

    init()
    files = (x for x in Path(path).iterdir() if x.is_file())

    for file in files:
        file_name = str(file.resolve())
        print("Processing file", file_name, "...")

        img = cv2.imread(file_name)
        face_locations = face_detector(img, 1)
        for (k, face) in enumerate(face_locations):
            if use_cuda:
                raw_shape = shape_predictor(img, face.rect)
            else:
                raw_shape = shape_predictor(img, face)
            face_descriptor = facerec.compute_face_descriptor(img, raw_shape)
            face_emb = vec2list(face_descriptor)

            if len(face_emb) == 128:
                file_name = file.name if k == 0 else f"{file.name}_{k + 1}"
                insert_data(dataset, file_name, face_emb)
        # try:
        #     print()
        # except:
        #     print(f"Processing error! {file_name}")
        return
