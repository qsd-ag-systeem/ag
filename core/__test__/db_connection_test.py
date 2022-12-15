import core.db as db
from pytest import fixture

def test_db_connection():
    assert db is not None
    assert db.engine is not None
    assert db.Session is not None
    assert db.Base is not None