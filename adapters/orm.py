from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from domain.models import Pet, Appointment, Service

Base = declarative_base()

class PetOrm(Base, Pet):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    species = Column(String)
    breed = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    appointments = relationship("AppointmentOrm", back_populates="pet")

class AppointmentOrm(Base, Appointment):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey('pets.id'))
    date = Column(String)
    reason = Column(String)
    pet = relationship("PetOrm", back_populates="appointments")

class ServiceOrm(Base, Service):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float) 