from unittest.mock import MagicMock, patch
from core.EsConnection import EsConnection
from core.search import retrieve_data, retrieve_all_data

class TestRetrieveData:
    @patch('core.search.EsConnection', spec=EsConnection)
    def test_retrieve_data(self, mock_es):
        mock_connection = MagicMock()
        mock_connection.search.return_value = {"hits": {"hits": [{"_source": "data"}]}}
        mock_es.return_value.connection = mock_connection

        face_emb = [1, 2, 3]
        datasets = ("dataset1", "dataset2")
        result = retrieve_data(face_emb, datasets)

        mock_connection.search.assert_called_once_with(
            index=mock_es.return_value.index_name,
            size=mock_es.return_value.default_size,
            source_excludes=["face_embedding"],
            knn={
                "field": "face_embedding",
                "query_vector": face_emb,
                "k": 100,
                "num_candidates": 100,
                "filter": {
                    "terms": {
                        "dataset": list(datasets)
                    }
                }
            }
        )

        assert result == {"hits": {"hits": [{"_source": "data"}]}}

    @patch('core.search.EsConnection', spec=EsConnection)
    def test_retrieve_all_data(self, mock_es):
        mock_connection = MagicMock()
        mock_connection.search.return_value = {"hits": {"hits": [{"_source": "data"}]}}
        mock_es.return_value.connection = mock_connection

        face_emb = [1, 2, 3]
        result = retrieve_all_data(face_emb)

        mock_connection.search.assert_called_once_with(
            index=mock_es.return_value.index_name,
            size=mock_es.return_value.default_size,
            source_excludes=["face_embedding"],
            knn={
                "field": "face_embedding",
                "query_vector": face_emb,
                "k": mock_es.return_value.default_size,
                "num_candidates": 100
            }
        )

        assert result == {"hits": {"hits": [{"_source": "data"}]}}