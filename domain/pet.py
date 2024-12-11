from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    species = Column(String)
    breed = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    # Foreign key to associate pet with user
    user_id = Column(Integer, ForeignKey('users.id'))  # Assuming 'users' is the table name for User
    user = relationship("User", back_populates="pets")  # Establish relationship with User
    # Relationships
    appointments = relationship("Appointment", back_populates="pet")