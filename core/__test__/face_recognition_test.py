from core.face_recognition import insert_data, init, vec2list, process_file
from dlib import vector
from click.testing import CliRunner
import os
from pathlib import Path

def test_insert_data():
    dataset = "test"
    file_name = "test.jpg"
    face_emb = vec2list([1, 2, 3])
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

def test_process_file_not_supported():
    runner = CliRunner()

    with runner.isolated_filesystem():
        os.mkdir('exists')
        with open('exists/test.txt', 'w') as f:
            f.write('test')

            file = Path('exists/test.txt')
            try:
                res = process_file("test", file)
                assert False
            except Exception as e:
                assert True
                assert "File not supported" in str(e)