import numpy as np

from core.face_recognition import insert_data, init, vec2list
from dlib import vector


def test_insert_data():
    dataset = "test"
    file_name = "test.jpg"
    face_emb = vec2list(np.arange(128))
    width = 100
    height = 100
    x = (0, 0)
    y = (0, 0)
    insert_data(dataset, file_name, face_emb, width, height, x, y)

    assert True


def test_init():
    res = init(False)
    assert res is None


def test_vec2list():
    vec = vector([1, 0])
    res = vec2list(vec)
    assert res == [1, 0]
