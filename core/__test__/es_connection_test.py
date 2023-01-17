from core.EsConnection import EsConnection
from pytest import fixture

@fixture
def db():
    return EsConnection()

def test_db_connection(db: EsConnection):
    assert db is not None
    assert db.connection is not None

def test_db_connection_string(db: EsConnection):
    assert str(db) is not None
    assert "EsConnection" in str(db)