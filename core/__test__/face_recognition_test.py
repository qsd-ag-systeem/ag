from unittest.mock import MagicMock, call, patch
from unittest import TestCase
from pathlib import Path
from core.EsConnection import EsConnection
from core.face_recognition import use_cuda, insert_data, init, process_file, search_file, get_face_embeddings

class TestFaceRecognition(TestCase):

    @patch('core.face_recognition.dlib.DLIB_USE_CUDA', True)
    def test_use_cuda_with_DLIB_USE_CUDA(self):
        assert use_cuda() is False
        assert use_cuda(enable_cuda=True) is True
        assert use_cuda(enable_cuda=False) is False

    @patch('core.face_recognition.dlib.DLIB_USE_CUDA', False)
    def test_use_cuda_withiout_DLIB_USE_CUDA(self):
        assert use_cuda() is False
        assert use_cuda(enable_cuda=True) is False
        assert use_cuda(enable_cuda=False) is False

    @patch('core.face_recognition.EsConnection', spec=EsConnection)
    def test_insert_data(self, mock_es):
        mock_es.return_value.connection.update.return_value = None

        dataset = "dataset1"
        file_name = "image1.jpg"
        face_emb = [1, 2, 3]
        width = 100
        height = 150
        x = (1, 2)
        y = (3, 4)
        key = 0

        insert_data(dataset, file_name, face_emb, width, height, x, y, key)

        mock_es.return_value.connection.update.assert_called_once_with(
            index=mock_es.return_value.index_name,
            id=f"{dataset}/{file_name}-{key}",
            doc={
                "dataset": dataset,
                "file_name": file_name,
                "width": width,
                "height": height,
                "top_left": x,
                "bottom_right": y,
                "face_embedding": face_emb,
            },
            doc_as_upsert=True
        )

    @patch('core.face_recognition.dlib')
    def test_init(self, mock_dlib):
        mock_dlib.face_recognition_model_v1.return_value = MagicMock()
        mock_dlib.shape_predictor.return_value = MagicMock()
        mock_dlib.get_frontal_face_detector.return_value = MagicMock()

        init(cuda=False)

        assert mock_dlib.face_recognition_model_v1.called
        assert mock_dlib.shape_predictor.called
        assert mock_dlib.get_frontal_face_detector.called

    @patch('core.face_recognition.dlib')
    def test_init_cuda(self, mock_dlib):
        mock_dlib.face_recognition_model_v1.return_value = MagicMock()
        mock_dlib.shape_predictor.return_value = MagicMock()
        mock_dlib.cnn_face_detection_model_v1.return_value = MagicMock()

        init(cuda=True)

        assert mock_dlib.face_recognition_model_v1.called
        assert mock_dlib.shape_predictor.called
        assert mock_dlib.cnn_face_detection_model_v1.called

    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file(self, mock_insert_data, mock_get_face_embeddings):
        face_embedding = [1, 2, 3]
        width = 100
        height = 150
        x = (1, 2)
        y = (3, 4)
        key = 0

        mock_get_face_embeddings.return_value = [
            {
                "face_embedding": face_embedding,
                "width": width,
                "height": height,
                "x": x,
                "y": y,
            }
        ]

        dataset = "dataset1"
        file = Path("image1.jpg")

        assert process_file(dataset, file, cuda=False) is True
        assert mock_insert_data.call_count == 1
        mock_insert_data.assert_called_once_with(
            dataset,
            file.name,
            face_embedding,
            width,
            height,
            x,
            y,
            key
        )

class TestFaceRecognitionSearchFile(TestCase):

    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.retrieve_data')
    @patch('core.face_recognition.retrieve_all_data')
    def test_search_file(self, mock_retrieve_all_data, mock_retrieve_data, mock_get_face_embeddings):
        file_name = "image1.jpg"
        face_embeddings = [
            {
                "face_embedding": [1, 2, 3],
                "width": 100,
                "height": 150,
                "x": (1, 2),
                "y": (3, 4),
            }
        ]
        dataset = ("dataset1", "dataset2")
        expected_results_dataset = [[file_name, "_id", "dataset", "file_name", round(1 * 100), "(1,2)", "(3,4)"]]
        expected_results_no_dataset = [[file_name, "_id", "dataset", "file_name", round(1 * 100), "(1,2)", "(3,4)"]]
        file = Path(file_name)
        mock_get_face_embeddings.return_value = face_embeddings

        retrieve_data_response = {
            "hits": {
                "hits": [
                    {                        
                        "_id": "_id",
                        "_source": {
                            "dataset": "dataset",
                            "file_name": "file_name",
                            "top_left": "(1,2)",
                            "bottom_right": "(3,4)"
                        },
                        "_score": 1
                    }
                ]
            }
        }

        mock_retrieve_data.return_value = retrieve_data_response
        mock_retrieve_all_data.return_value = retrieve_data_response
        
        results = search_file(file, dataset=dataset, cuda=False)
        assert results == expected_results_dataset
        mock_retrieve_data.assert_called_once()

        mock_retrieve_data.reset_mock()
        results = search_file(file, dataset=None, cuda=False)
        assert results == expected_results_no_dataset
        mock_retrieve_all_data.assert_called_once()

class TestFaceRecognitionGetFaceEmbedding(TestCase):
    class MockImage:
        def __init__(self, shape):
            self.shape = shape

    class MockRectangle:
        def __init__(self, left, top, right, bottom):
            self._left = left
            self._top = top
            self._right = right
            self._bottom = bottom

        def left(self):
            return self._left

        def top(self):
            return self._top

        def right(self):
            return self._right

        def bottom(self):
            return self._bottom

    class MockFullObjectDetection:
        def __init__(self, rect, parts):
            self.rect = rect
            self.parts = parts

    img_height = 100
    img_width = 90
    img = MockImage((img_height, img_width, 3))
    face_embedding = [*range(128)]

    face1_width = 50
    face1_height = 50
    face1_x = 0
    face1_y = 0
    mock_rectangle1 = MockRectangle(face1_x, face1_y, face1_x + face1_width, face1_y + face1_height)
    mock_full_object_detection1 = MockFullObjectDetection(mock_rectangle1, range(68))

    face2_width = 50
    face2_height = 50
    face2_x = 50
    face2_y = 50
    mock_rectangle2 = MockRectangle(face2_x, face2_y, face2_x + face2_width, face2_y + face2_height)
    mock_full_object_detection2 = MockFullObjectDetection(mock_rectangle2, range(68))

    @patch('core.face_recognition.face_detector')
    @patch('core.face_recognition.shape_predictor')
    @patch('core.face_recognition.facerec')
    def test_get_face_embeddings_one_face(self, mock_facerec, mock_shape_predictor, mock_face_detector):
        mock_face_detector.return_value = [self.mock_rectangle1]
        mock_shape_predictor.return_value = self.mock_rectangle1
        mock_facerec.compute_face_descriptor.return_value = self.face_embedding

        faces = get_face_embeddings(self.img, False)

        assert len(faces) == 1
        assert faces[0]["width"] == self.img_width
        assert faces[0]["height"] == self.img_height
        assert faces[0]["x"] == (self.mock_rectangle1.left(), self.mock_rectangle1.top())
        assert faces[0]["y"] == (self.mock_rectangle1.right(), self.mock_rectangle1.bottom())
        assert faces[0]["face_embedding"] == self.face_embedding

        mock_face_detector.assert_called_once()
        mock_shape_predictor.assert_called_once()
        mock_facerec.compute_face_descriptor.assert_called_once_with(self.img, self.mock_rectangle1)

    @patch('core.face_recognition.shape_predictor')
    @patch('core.face_recognition.face_detector')
    @patch('core.face_recognition.facerec')
    def test_get_face_embeddings_multiple_faces(self, mock_facerec, mock_face_detector, mock_shape_predictor):
        mock_face_detector.return_value = [
            self.mock_rectangle1, 
            self.mock_rectangle2]

        mock_shape_predictor.side_effect = [
            self.mock_rectangle1,
            self.mock_rectangle2]
        
        mock_facerec.compute_face_descriptor.return_value = self.face_embedding

        faces = get_face_embeddings(self.img, False)
        assert len(faces) == 2

        assert faces[0]["width"] == self.img_width
        assert faces[0]["height"] == self.img_height
        assert faces[0]["x"] == (self.face1_x, self.face1_y)
        assert faces[0]["y"] == (self.face1_x + self.face1_width, self.face1_y + self.face1_height)

        assert faces[1]["width"] == self.img_width
        assert faces[1]["height"] == self.img_height
        assert faces[1]["x"] == (self.face2_x, self.face2_y)
        assert faces[1]["y"] == (self.face2_x + self.face2_width, self.face2_y + self.face2_height)
    
        mock_face_detector.assert_called_once_with(self.img, 1)
        mock_shape_predictor.assert_has_calls([
            call(self.img, self.mock_rectangle1),
            call(self.img, self.mock_rectangle2)])

        mock_facerec.compute_face_descriptor.assert_has_calls([
            call(self.img, self.mock_rectangle1),
            call(self.img, self.mock_rectangle2)])

    @patch('core.face_recognition.shape_predictor')
    @patch('core.face_recognition.face_detector')
    @patch('core.face_recognition.facerec')
    def test_get_face_embeddings_no_face(self, mock_shape_predictor, mock_face_detector, mock_facerec):
        mock_face_detector.side_effect = RuntimeError()

        with self.assertRaises(Exception) as e:
            faces = get_face_embeddings(self.img, False)

            assert str(e.exception) == "Unable to detect face locations"
            mock_face_detector.assert_called_once_with(self.img, 1)
            mock_shape_predictor.assert_not_called()
            mock_facerec.compute_face_descriptor.assert_not_called()

    @patch('core.face_recognition.shape_predictor')
    @patch('core.face_recognition.face_detector')
    @patch('core.face_recognition.facerec')
    def test_get_face_embedding_cuda_enabled(self, mock_facerec, mock_face_detector, mock_shape_predictor):
        mock_face_detector.return_value = [self.mock_full_object_detection1]
        mock_shape_predictor.return_value = self.mock_rectangle1
        mock_facerec.compute_face_descriptor.return_value = self.face_embedding

        faces = get_face_embeddings(self.img, True)

        assert len(faces) == 1
        
        assert faces[0]["width"] == self.img_width
        assert faces[0]["height"] == self.img_height
        assert faces[0]["x"] == (self.mock_rectangle1.left(), self.mock_rectangle1.top())
        assert faces[0]["y"] == (self.mock_rectangle1.right(), self.mock_rectangle1.bottom())
        assert faces[0]["face_embedding"] == self.face_embedding

        mock_face_detector.assert_called_once()
        mock_shape_predictor.assert_called_once()
        mock_facerec.compute_face_descriptor.assert_called_once_with(self.img, self.mock_rectangle1)

