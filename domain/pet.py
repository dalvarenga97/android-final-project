from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Pet(Base):
    __tablename__ = 'pets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    
    # Foreign key to associate pet with user
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Assuming 'users' is the table name for User
    user = relationship("User", back_populates="pets")  # Establish relationship with User

    # Relationships
    appointments = relationship("Appointment", back_populates="pet")
