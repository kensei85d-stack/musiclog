from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.dependencies.auth import get_current_user
import backend.app.crud.history as crud
from backend.app.schemas.history import HistoryCreate, HistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


# 再生履歴を追加（認証必須）
@router.post("/", response_model=HistoryResponse)
def add_history(
    data: HistoryCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return crud.create_history(db, user_id, data)


# 自分の再生履歴を取得（認証必須）
@router.get("/", response_model=list[HistoryResponse])
def get_my_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return crud.get_history_by_user(db, user_id)
