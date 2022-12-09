from core import DbConnection

def test_db_connection():
    db = DbConnection.DbConnection()
    assert db is not None
    assert db.connection is not None
    assert db.cursor is not None

def test_db_connection_string():
    db = DbConnection.DbConnection()
    assert str(db) is not None
    assert "DbConnection" in str(db)