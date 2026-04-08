from sqlalchemy.orm import Session
from backend.app.models.Play_history import PlayHistory
from backend.app.schemas.history import HistoryCreate

def create_history(db: Session, user_id: int, data: HistoryCreate):
    history = PlayHistory(
        user_id=user_id,
        track_id=data.track_id
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_history_by_user(db: Session, user_id: int):
    return db.query(PlayHistory).filter(PlayHistory.user_id == user_id).all()
