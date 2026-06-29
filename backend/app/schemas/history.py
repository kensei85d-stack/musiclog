from pydantic import BaseModel
from datetime import datetime

class HistoryCreate(BaseModel):
    track_id: int

class HistoryResponse(BaseModel):
    id: int
    user_id: int
    track_id: int
    played_at: datetime

    class Config:
        from_attributes = True
