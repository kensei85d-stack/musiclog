from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models import Base

class PlayHistory(Base):
    __tablename__ = "play_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    played_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="play_histories")
    track = relationship("Track", back_populates="play_histories")