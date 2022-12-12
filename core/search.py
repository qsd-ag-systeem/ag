from core.DbConnection import DbConnection


def retrieve_data(face_emb: list, datasets: tuple):
    db = DbConnection()
    db_cursor = db.cursor

    query_string = "SELECT id, dataset, file_name, x, y, euclidian(%s, face_embedding) AS eucl FROM faces WHERE dataset IN (%s) ORDER BY eucl ASC LIMIT 1000;"
    db_cursor.execute(query_string, ((str(face_emb).replace('[', '{').replace(']', '}'),), datasets))
    result = db_cursor.fetchall()
    return result


def retrieve_all_data(face_emb: list):
    db = DbConnection()
    db_cursor = db.cursor

    query_string = "SELECT id, dataset, file_name, x, y, euclidian(%s, face_embedding) AS eucl FROM faces ORDER BY eucl ASC LIMIT 1000;"
    db_cursor.execute(query_string, (str(face_emb).replace('[', '{').replace(']', '}'),))
    result = db_cursor.fetchall()
    return result


def retrieve_datasets():
    db = DbConnection()
    db_cursor = db.cursor

    query_string = "SELECT dataset, COUNT(dataset) AS count FROM faces GROUP BY dataset"

    db_cursor.execute(query_string)
    result = db_cursor.fetchall()
    return result

def delete_dataset(dataset: str):
    db = DbConnection()
    db_cursor = db.cursor

    query_string = "DELETE FROM faces WHERE dataset = %s"
    db_cursor.execute(query_string, (dataset,))