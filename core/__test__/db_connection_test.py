from core.DbConnection import DbConnection
from pytest import fixture


@fixture
def db():
    return DbConnection()


def test_db_connection(db: DbConnection):
    assert db is not None
    assert db.connection is not None
    assert db.cursor is not None


def test_db_connection_string(db: DbConnection):
    assert str(db) is not None
    assert "DbConnection" in str(db)
