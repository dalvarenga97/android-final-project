from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    date = Column(String, nullable=False)
    reason = Column(String, nullable=False)

    # Relationship with Pet
    pet = relationship("Pet", back_populates="appointments")
