from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, DOUBLE_PRECISION
from core.db import Base
from core.pg_point import Point

class Face(Base):
    __tablename__ = 'faces'
    id = Column(Integer, primary_key=True)
    dataset = Column(String(100))
    file_name = Column(String(100))
    width = Column(Integer)
    height = Column(Integer)
    x = Column(Point)
    y = Column(Point)
    face_embedding = Column(ARRAY(DOUBLE_PRECISION))

    def __init__(self, dataset, file_name, width, height, x, y, face_embedding):
        self.dataset = dataset
        self.file_name = file_name
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.face_embedding = face_embedding