from core.DbConnection import DbConnection


def retrieve_data(face_emb, datasets):
    try:
        db = DbConnection()
        db_cursor = db.cursor

        where_string = ""

        if (datasets != None and datasets != ()):
            where_string = """
                WHERE dataset IN ('{0}')
            """.format("','".join(datasets))

        query_string = """
            SELECT id, dataset, file_name, x, y,
                euclidian('{0}', face_embedding) AS eucl 
            FROM faces
            {1}
            ORDER BY eucl ASC
            """.format(face_emb, where_string).replace('[', '{').replace(']', '}')
        db_cursor.execute(query_string)
        result = db_cursor.fetchall()
        return result
    except Exception as e:
        print(f"Select error {face_emb} ", e)


def retrieve_datasets():
    try:
        db = DbConnection()
        db_cursor = db.cursor

        query_string = """
            SELECT dataset,  COUNT(dataset) AS count
            FROM faces
            GROUP BY dataset
            """

        db_cursor.execute(query_string)
        result = db_cursor.fetchall()
        return result
    except Exception as e:
        print(f"Select error ", e)
