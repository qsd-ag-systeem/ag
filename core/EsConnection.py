from elasticsearch import Elasticsearch

class EsConnection(object):
    connection = None

    def __init__(self):
        try:
            self.connection = Elasticsearch([{'host': '127.0.0.1', 'port': 9200, 'scheme': 'http'}])
            pass
        except Exception as e:
            print("\nError while connecting to ES: ", e)
            exit(0)

    def __str__(self):
        return f"EsConnection: {self.connection}"
