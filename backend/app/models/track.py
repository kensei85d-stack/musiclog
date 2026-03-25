from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)

    artist = relationship("Artist", back_populates="tracks")
    play_histories = relationship("PlayHistory", back_populates="track")