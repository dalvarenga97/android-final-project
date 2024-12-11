from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from .base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(256))

    # Establish relationship with Pet
    pets = relationship("Pet", back_populates="user")  # Link to pets

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)