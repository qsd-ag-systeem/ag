import core.db as db


def export_all(file):
    raw_connection = db.engine.raw_connection()
    db_cursor = raw_connection.cursor()

    query = "COPY (SELECT dataset,file_name,width,height,x,y,face_embedding FROM faces) TO STDOUT WITH CSV"

    with open(file, 'w') as f:
        db_cursor.copy_expert(query, f)


def export_dataset(file, datasets: tuple):
    raw_connection = db.engine.raw_connection()
    db_cursor = raw_connection.cursor()

    query = db_cursor.mogrify(
        "COPY (SELECT dataset,file_name,width,height,x,y,face_embedding FROM faces WHERE dataset in (%s)) TO STDOUT WITH CSV",
        datasets
    )

    with open(file, 'w') as f:
        db_cursor.copy_expert(query, f)
