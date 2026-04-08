from pydantic import BaseModel

class HistoryCreate(BaseModel):
    track_id: int

class HistoryResponse(BaseModel):
    id: int
    user_id: int
    track_id: int

    class Config:
        orm_mode = True
