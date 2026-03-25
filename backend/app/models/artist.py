from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import Base

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    tracks = relationship("Track", back_populates="artist")