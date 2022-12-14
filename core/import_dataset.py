from core.DbConnection import DbConnection


def import_all(file):
    db = DbConnection()
    db_cursor = db.cursor

    with open(file) as f:
        db_cursor.copy_expert("copy faces (dataset,file_name,width,height,x,y,face_embedding) from stdin (format csv)", f)
        return
