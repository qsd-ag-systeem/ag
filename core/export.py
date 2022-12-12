from core.DbConnection import DbConnection


def export_all(file):
    db = DbConnection()
    db_cursor = db.cursor

    query = "COPY (SELECT * FROM faces) TO STDOUT WITH CSV HEADER"

    with open(file, 'w') as f:
        db_cursor.copy_expert(query, f)


def export_dataset(file, datasets: tuple):
    db = DbConnection()
    db_cursor = db.cursor

    query = db_cursor.mogrify("COPY (SELECT * FROM faces WHERE dataset in (%s)) TO STDOUT WITH CSV HEADER", datasets)

    with open(file, 'w') as f:
        db_cursor.copy_expert(query, f)
