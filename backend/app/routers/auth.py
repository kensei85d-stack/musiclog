from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.schemas.user import UserLogin
from backend.app.core.security import verify_password, create_access_token
from backend.app.core.database import get_db
from backend.app.crud.user import get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])

# ログイン（JWT を発行）
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    # email でユーザーを検索
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # パスワードを検証
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # JWT を作成（sub に user.id を入れる）
    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}
