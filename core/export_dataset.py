from core.DbConnection import DbConnection


def export_all(file):
    db = DbConnection()
    db_cursor = db.cursor

    query = "COPY (SELECT dataset,file_name,width,height,x,y,face_embedding FROM faces) TO STDOUT WITH CSV"

    if not file.endswith('.csv'):
        file = f"{file}.csv"

    with open(file, 'w') as f:
        db_cursor.copy_expert(query, f)


def export_dataset(file, datasets: tuple):
    db = DbConnection()
    db_cursor = db.cursor

    query = db_cursor.mogrify(
        "COPY (SELECT dataset,file_name,width,height,x,y,face_embedding FROM faces WHERE dataset in (%s)) TO STDOUT WITH CSV",
        datasets
    )

    if not file.endswith('.csv'):
        file = f"{file}.csv"

    with open(file, 'w') as f:
        db_cursor.copy_expert(query, f)
