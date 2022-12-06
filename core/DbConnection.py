import psycopg2


class DbConnection(object):
    connection = None
    cursor = None

    def __init__(self):
        con = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="postgres",
            password="postgres",
            connect_timeout=3
        )

        con.set_session(autocommit=True)

        self.connection = con
        self.cursor = con.cursor()

    def __str__(self):
        return self.connection
