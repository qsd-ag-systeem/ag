import os
import dlib
from pathlib import Path

ROOT_DIR = os.path.abspath(os.curdir)

face_rec_model_path = ROOT_DIR + \
    '/core/data/dlib_face_recognition_resnet_model_v1.dat'
predictor_path = ROOT_DIR + '/core/data/shape_predictor_5_face_landmarks.dat'
detector_path = ROOT_DIR + '/core/data/mmod_human_face_detector.dat'

facerec = dlib.face_recognition_model_v1(face_rec_model_path)
shape_predictor = dlib.shape_predictor(predictor_path)

if dlib.DLIB_USE_CUDA:
    print("⚡ Using CUDA!")
    detector = dlib.cnn_face_detection_model_v1(detector_path)
else:
    print("🐢 CUDA not available, falling back to CPU processing!")
    detector = dlib.get_frontal_face_detector()


def insert_data(dataset, name, face_emb):
    # Database insert ...
    print("")


def folder_exec(dataset, path):
    print("Processing directory", path, "...")
    files = (x for x in Path(path).iterdir() if x.is_file())
    for file in files:
        file_name = str(file.resolve())
        print("Processing file", file_name, "...")
        try:
            img = dlib.load_rgb_image(file_name)
            face_desc = get_face_embedding(img)
            face_emb = vec2list(face_desc)
            if len(face_emb) == 128:
                insert_data(dataset, file.name, face_emb)
        except:
            print(f"Processing error! {file_name}")
        return


def vec2list(vec):
    out_list = []
    for i in vec:
        out_list.append(i)
    return out_list


def get_face_embedding(img):
    face_descriptor = []
    try:
        dets = detector(img, 1)
        for k, d in enumerate(dets):
            shape = shape_predictor(img, d)
            try:
                face_descriptor = facerec.compute_face_descriptor(img, shape)
            except:
                face_descriptor = []
    except:
        face_descriptor = []
    return face_descriptor
