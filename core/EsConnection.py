from elasticsearch import Elasticsearch


class EsConnection(object):
    connection = None
    index_name = "face_recognition"
    default_size = 100
    default_scroll_time = "1m"
    default_timeout = 300

    def __init__(self):
        try:
            self.connection = Elasticsearch([{'host': '127.0.0.1', 'port': 9200, 'scheme': 'http'}])
            pass
        except Exception as e:
            print("\nError while connecting to ES: ", e)
            exit(0)

    def __str__(self):
        return f"EsConnection: {self.connection}"
