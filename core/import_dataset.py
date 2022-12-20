import core.db as db


def import_all(file):
    raw_connection = db.engine.raw_connection()
    db_cursor = raw_connection.cursor()

    with open(file) as f:
        db_cursor.copy_expert("copy faces (dataset,file_name,width,height,x,y,face_embedding) from stdin (format csv)", f)
        return
