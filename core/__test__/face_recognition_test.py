from unittest.mock import MagicMock, call, patch
from unittest import TestCase
from pathlib import Path
from core.EsConnection import EsConnection
from core.face_recognition import use_cuda, insert_data, init, process_file, search_file, get_face_embeddings

class MockImage:
    def __init__(self, shape):
        self.shape = shape

class TestFaceRecognition(TestCase):

    @patch('core.face_recognition.dlib.DLIB_USE_CUDA', True)
    def test_use_cuda_with_DLIB_USE_CUDA(self):
        self.assertFalse(use_cuda())
        self.assertTrue(use_cuda(enable_cuda=True))
        self.assertFalse(use_cuda(enable_cuda=False))

    @patch('core.face_recognition.dlib.DLIB_USE_CUDA', False)
    def test_use_cuda_without_DLIB_USE_CUDA(self):
        self.assertFalse(use_cuda())
        self.assertFalse(use_cuda(enable_cuda=True))
        self.assertFalse(use_cuda(enable_cuda=False))

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

        mock_dlib.face_recognition_model_v1.assert_called()
        mock_dlib.shape_predictor.assert_called()
        mock_dlib.get_frontal_face_detector.assert_called()

    @patch('core.face_recognition.dlib')
    def test_init_cuda(self, mock_dlib):
        mock_dlib.face_recognition_model_v1.return_value = MagicMock()
        mock_dlib.shape_predictor.return_value = MagicMock()
        mock_dlib.cnn_face_detection_model_v1.return_value = MagicMock()

        init(cuda=True)

        mock_dlib.face_recognition_model_v1.assert_called()
        mock_dlib.shape_predictor.assert_called()
        mock_dlib.cnn_face_detection_model_v1.assert_called()

class TestFaceRecognitionProcessFile(TestCase):
    face_embedding = [1, 2, 3]
    width = 100
    height = 150
    x = (1, 2)
    y = (3, 4)
    key = 0

    dataset = "dataset1"
    file = Path("image1.jpg")
    img = MockImage((100, 100, 3))

    face_embedding_return_1 = [
            {
                "face_embedding": face_embedding,
                "width": width,
                "height": height,
                "x": x,
                "y": y,
            }
        ]

    face_embedding_return_2 = [
            {
                "face_embedding": face_embedding,
                "width": width,
                "height": height,
                "x": x,
                "y": y,
            },
            {
                "face_embedding": face_embedding,
                "width": width,
                "height": height,
                "x": x,
                "y": y,
            }
        ]

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file(self, mock_insert_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img

        mock_get_face_embeddings.return_value = self.face_embedding_return_1

        process_file(self.dataset, self.file, cuda=False)

        self.assertEqual(mock_insert_data.call_count, 1)
        mock_insert_data.assert_called_once_with(
            self.dataset,
            self.file.name,
            self.face_embedding,
            self.width,
            self.height,
            self.x,
            self.y,
            self.key
        )
    
    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file_file_not_exists(self, mock_insert_data, mock_get_face_embeddings, mock_imread):
        mock_file = MagicMock()
        mock_file.resolve.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError) as context:
            process_file(self.dataset, mock_file, cuda=False)

        mock_insert_data.assert_not_called()
        mock_get_face_embeddings.assert_not_called()


    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file_no_faces(self, mock_insert_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img
        mock_get_face_embeddings.return_value = []

        process_file(self.dataset, self.file, cuda=False)

        mock_insert_data.assert_not_called()

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file_get_face_embedding_exception(self, mock_insert_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img
        mock_get_face_embeddings.side_effect = Exception

        with self.assertRaises(Exception) as context:
            process_file(self.dataset, self.file, cuda=False)

        mock_insert_data.assert_not_called()

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file_insert_data_exception(self, mock_insert_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img
        mock_get_face_embeddings.return_value = self.face_embedding_return_2
        mock_insert_data.side_effect = [Exception, None]

        with self.assertRaises(Exception) as context:
            process_file(self.dataset, self.file, cuda=False)

        self.assertIn(str([(0, self.face_embedding_return_2[0])]), str(context.exception))

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file_cuda_true(self, mock_insert_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img
        mock_get_face_embeddings.return_value = self.face_embedding_return_1

        process_file(self.dataset, self.file, cuda=True)
        
        mock_insert_data.assert_called_once()
        mock_get_face_embeddings.assert_called_once_with(self.img, True)

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.insert_data')
    def test_process_file_multiple_faces(self, mock_insert_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img
        mock_get_face_embeddings.return_value = self.face_embedding_return_2

        process_file(self.dataset, self.file, cuda=False)
        
        self.assertEqual(mock_insert_data.call_count, 2)
        mock_get_face_embeddings.assert_called_once()

class TestFaceRecognitionSearchFile(TestCase):

    file_name = "image1.jpg"
    file = Path(file_name)
    img = MockImage((100, 100, 3))

    face_embedding_1_face = [
            {
                "face_embedding": [1, 2, 3],
                "width": 100,
                "height": 150,
                "x": (1, 2),
                "y": (3, 4),
            }
        ]
    
    face_embedding_2_face = [
            {
                "face_embedding": [1, 2, 3],
                "width": 100,
                "height": 150,
                "x": (1, 2),
                "y": (3, 4),
            },
            {
                "face_embedding": [4, 5, 6],
                "width": 100,
                "height": 150,
                "x": (5, 6),
                "y": (7, 8),
            }
        ]

    dataset = ("dataset1", "dataset2")

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.retrieve_knn_filtered_search_data')
    @patch('core.face_recognition.retrieve_knn_search_data')
    def test_search_file_success(self, mock_retrieve_knn_search_data, mock_retrieve_knn_filtered_search_data, mock_get_face_embeddings, mock_imread):
        expected_results_dataset = [[self.file_name, "_id", "dataset", "file_name", round(1 * 100), "(1,2)", "(3,4)"]]
        expected_results_no_dataset = [[self.file_name, "_id", "dataset", "file_name", round(1 * 100), "(1,2)", "(3,4)"]]
        mock_get_face_embeddings.return_value = self.face_embedding_1_face
        mock_imread.return_value = self.img

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

        mock_retrieve_knn_filtered_search_data.return_value = retrieve_data_response
        mock_retrieve_knn_search_data.return_value = retrieve_data_response
        
        results = search_file(self.file, dataset=self.dataset, cuda=False)
        self.assertEqual(results, expected_results_dataset)
        mock_retrieve_knn_filtered_search_data.assert_called_once()

        mock_retrieve_knn_filtered_search_data.reset_mock()
        results = search_file(self.file, dataset=None, cuda=False)
        self.assertEqual(results, expected_results_no_dataset)
        mock_retrieve_knn_search_data.assert_called_once()

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.retrieve_knn_filtered_search_data')
    @patch('core.face_recognition.retrieve_knn_search_data')
    def test_search_file_no_faces(self, mock_retrieve_knn_search_data, mock_retrieve_knn_filtered_search_data, mock_get_face_embeddings, mock_imread):
        mock_get_face_embeddings.side_effect = Exception("No faces found")
        mock_imread.return_value = self.img

        mock_retrieve_knn_filtered_search_data.assert_not_called()
        mock_retrieve_knn_search_data.assert_not_called()

        with self.assertRaises(Exception) as context:
            search_file(self.file, dataset=self.dataset, cuda=False)
        
        self.assertTrue("No faces found" in str(context.exception))

        with self.assertRaises(Exception) as context:
            search_file(self.file, dataset=None, cuda=False)

        self.assertTrue("No faces found" in str(context.exception))

    def test_search_file_invalid_image(self):
        file = MagicMock()
        file.resolve.side_effect = Exception("File not supported")

        with self.assertRaises(Exception) as context:
            search_file(file, dataset=None, cuda=False)
        self.assertEqual(str(context.exception), "File not supported")

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.retrieve_knn_filtered_search_data')
    @patch('core.face_recognition.retrieve_knn_search_data')
    def test_search_file_cuda_enabled(self, mock_retrieve_knn_search_data, mock_retrieve_knn_filtered_search_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img

        mock_get_face_embeddings.return_value = self.face_embedding_1_face
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
        mock_retrieve_knn_filtered_search_data.return_value = retrieve_data_response
        mock_retrieve_knn_search_data.return_value = retrieve_data_response

        search_file(self.file, dataset=None, cuda=True)

        mock_get_face_embeddings.assert_called_with(self.img, True)

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.retrieve_knn_filtered_search_data')
    @patch('core.face_recognition.retrieve_knn_search_data')
    def test_search_file_exception_in_retrieval(self, mock_retrieve_knn_search_data, mock_retrieve_knn_filtered_search_data, mock_get_face_embeddings, mock_imread):
        mock_imread.return_value = self.img
                
        retrieve_data_response = {
            "hits": {
                "hits": [
                    {                        
                        "_id": "_id2",
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

        mock_get_face_embeddings.return_value = self.face_embedding_2_face
        
        mock_retrieve_knn_filtered_search_data.side_effect = [Exception, retrieve_data_response]
        mock_retrieve_knn_search_data.side_effect = Exception

        results = search_file(self.file, dataset=self.dataset, cuda=False)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "_id2")

    @patch('cv2.imread')
    @patch('core.face_recognition.get_face_embeddings')
    @patch('core.face_recognition.retrieve_knn_filtered_search_data')
    @patch('core.face_recognition.retrieve_knn_search_data')
    def test_search_file_empty_result(self, mock_retrieve_knn_search_data, mock_retrieve_knn_filtered_search_data, mock_get_face_embeddings, mock_imread):
        expected_results = []

        mock_imread.return_value = self.img
        mock_get_face_embeddings.return_value = self.face_embedding_1_face
        mock_retrieve_knn_filtered_search_data.return_value = {"hits": {"hits": []}}
        mock_retrieve_knn_search_data.return_value = {"hits": {"hits": []}}

        results = search_file(self.file, dataset=self.dataset, cuda=False)
        self.assertEqual(results, expected_results)

class TestFaceRecognitionGetFaceEmbedding(TestCase):
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

        self.assertEqual(len(faces), 1)
        self.assertEqual(faces[0]["width"], self.img_width)
        self.assertEqual(faces[0]["height"], self.img_height)
        self.assertEqual(faces[0]["x"], (self.mock_rectangle1.left(), self.mock_rectangle1.top()))
        self.assertEqual(faces[0]["y"], (self.mock_rectangle1.right(), self.mock_rectangle1.bottom()))
        self.assertEqual(faces[0]["face_embedding"], self.face_embedding)

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
        self.assertEqual(len(faces), 2)

        self.assertEqual(faces[0]["width"], self.img_width)
        self.assertEqual(faces[0]["height"], self.img_height)
        self.assertEqual(faces[0]["x"], (self.face1_x, self.face1_y))
        self.assertEqual(faces[0]["y"], (self.face1_x + self.face1_width, self.face1_y + self.face1_height))

        self.assertEqual(faces[1]["width"], self.img_width)
        self.assertEqual(faces[1]["height"], self.img_height)
        self.assertEqual(faces[1]["x"], (self.face2_x, self.face2_y))
        self.assertEqual(faces[1]["y"], (self.face2_x + self.face2_width, self.face2_y + self.face2_height))
    
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

            self.assertEqual(str(e.exception), "Unable to detect face locations")
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

        self.assertEqual(len(faces), 1)
        
        self.assertEqual(faces[0]["width"], self.img_width)
        self.assertEqual(faces[0]["height"], self.img_height)
        self.assertEqual(faces[0]["x"], (self.mock_rectangle1.left(), self.mock_rectangle1.top()))
        self.assertEqual(faces[0]["y"], (self.mock_rectangle1.right(), self.mock_rectangle1.bottom()))
        self.assertEqual(faces[0]["face_embedding"], self.face_embedding)

        mock_face_detector.assert_called_once()
        mock_shape_predictor.assert_called_once()
        mock_facerec.compute_face_descriptor.assert_called_once_with(self.img, self.mock_rectangle1)