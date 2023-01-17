from unittest.mock import MagicMock, patch
from unittest import TestCase

from elasticsearch import NotFoundError
from core.delete import delete_dataset_by_name, delete_dataset_file_by_name, delete_dataset_files_by_name, delete_file_by_name

class TestDeleteFile(TestCase):


    @patch('core.delete.dataset_exists')
    def test_delete_file_by_name_dataset_not_exists(self, mock_dataset_exists):
        mock_dataset_exists.return_value = False

        dataset = "dataset"
        file_name = "image.jpg"

        with self.assertRaises(Exception) as context:
            delete_file_by_name(dataset, file_name)

        self.assertIn("Dataset '{}' does not exist.".format(dataset), str(context.exception))
        

    @patch('core.delete.dataset_exists')
    @patch('core.delete.EsConnection')
    def test_delete_file_by_name_query_called_with_correct_args(self, mock_es_conn, mock_dataset_exists):
        mock_dataset_exists.return_value = True
        mock_es_conn.return_value = mock_es_conn
        mock_es_conn.index_name = "face_embeddings"

        dataset = 'dataset1'
        file_name = 'image1.jpg'
        delete_file_by_name(dataset, file_name)

        print(mock_es_conn.connection.delete_by_query.call_args_list)
        mock_es_conn.connection.delete_by_query.assert_called_once_with(index='face_embeddings', query={
            "bool": {
                "must": [
                    {
                        "term": {
                            "dataset": dataset,
                        },
                    },
                    {
                        "term": {
                            "file_name": file_name,
                        },
                    }
                ]
            }
        })

class TestDeleteDataset(TestCase):
    @patch('core.delete.dataset_exists')
    def test_delete_dataset_by_name_dataset_not_exists(self, mock_dataset_exists):
        mock_dataset_exists.return_value = False
        dataset = "dataset"

        with self.assertRaises(Exception) as context:
            delete_dataset_by_name(dataset)

        self.assertIn("Dataset '{}' does not exist.".format(dataset), str(context.exception))
        

    @patch('core.delete.dataset_exists')
    @patch('core.delete.EsConnection')
    def test_delete_dataset_by_name_query_called_with_correct_args(self, mock_es_conn, mock_dataset_exists):
        mock_dataset_exists.return_value = True
        mock_es_conn.return_value = mock_es_conn
        mock_es_conn.index_name = "face_embeddings"

        dataset = 'dataset1'

        delete_dataset_by_name(dataset)

        print(mock_es_conn.connection.delete_by_query.call_args_list)
        mock_es_conn.connection.delete_by_query.assert_called_once_with(index='face_embeddings', query={
            "term": {
                "dataset": dataset,
            },
        })