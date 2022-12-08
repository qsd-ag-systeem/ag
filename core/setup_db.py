import os
from core.db import Session, engine, Base
from core.model.face import Face

def setup_db():
    root_dir = os.path.abspath(os.curdir)

    Base.metadata.create_all(engine)
    session = Session()
    
    session.execute(open(root_dir + "/core/sql/euclidian_func.sql", "r").read())
    session.execute(open(root_dir + "/core/sql/vec_sub_func.sql", "r").read())

    session.commit()
    session.close()
