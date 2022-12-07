from psycopg2 import connect, Error


class DbConnection(object):
    connection = None
    cursor = None

    def __init__(self):
        try:
            con = connect(
                host="127.0.0.1",
                database="postgres",
                user="postgres",
                password="postgres",
                connect_timeout=3
            )
            con.set_session(autocommit=True)

            self.connection = con
            self.cursor = con.cursor()
        except Error as e:
            print("\nError while connecting to PostgreSQL: ", e)
            exit(0)

    def __str__(self):
        return f"DbConnection: {self.connection}, {self.cursor}"
