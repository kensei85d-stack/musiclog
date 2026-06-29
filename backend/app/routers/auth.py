from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.schemas.user import (
    UserLogin,
    UserCreate,
    UserRead,
    Token,
    TokenRefresh,
)
from backend.app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from backend.app.core.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.crud.user import get_user_by_email, create_user, get_user_by_id

router = APIRouter(prefix="/auth", tags=["auth"])

# 新規登録
@router.post("/signup", response_model=UserRead)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="User with this email already exists")
    user = create_user(db, data)
    return user


# ログイン（JWT を発行）
@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# ログイン済みユーザー情報
@router.get("/me", response_model=UserRead)
def me(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# リフレッシュトークンで再発行
@router.post("/refresh", response_model=Token)
def refresh_token(data: TokenRefresh, db: Session = Depends(get_db)):
    payload = decode_access_token(data.refresh_token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = get_user_by_id(db, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
