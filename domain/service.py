from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float) 