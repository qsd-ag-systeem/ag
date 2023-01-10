from unittest.mock import MagicMock, patch
import numpy as np
from pathlib import Path
from core.EsConnection import EsConnection
from core.face_recognition import use_cuda, insert_data, init, process_file, search_file, get_face_embeddings


class TestFaceRecognition:
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
                        "_score": 1,
                    }
                ]
            }
        }

        mock_retrieve_data.return_value = retrieve_data_response
        mock_retrieve_all_data.return_value = retrieve_data_response
        
        # check function output with dataset
        results = search_file(file, dataset=dataset, cuda=False)
        assert results == expected_results_dataset
        mock_retrieve_data.assert_called_once()

        # check function output without dataset
        mock_retrieve_data.reset_mock()
        results = search_file(file, dataset=None, cuda=False)
        assert results == expected_results_no_dataset
        mock_retrieve_all_data.assert_called_once()

                       
    @patch("dlib.rectangle")
    @patch("dlib.full_object_detection")
    def test_get_face_embeddings(self, detection_mock, rectangle_mock):
        img = MagicMock()
        shape = (3, 4, 3)
        img.shape = shape
        width, height, _ = shape
        rectangle_mock.return_value = (1, 2, 3, 4)
        detection_mock.return_value = [1, 2, 3]
        expected_face_embeddings = [
            {"face_embedding": [1, rectangle_mock, 3], "width": width, "height": height, "x": (1, 2), "y": (3, 4)}
        ]

        results = get_face_embeddings(img, False)
        assert results == expected_face_embeddings

