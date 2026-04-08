from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.core.security import hash_password

# ユーザー作成（新規登録）
def create_user(db: Session, data: UserCreate):
    hashed_pw = hash_password(data.password)
    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hashed_pw,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# email でユーザーを取得（ログインで使用）
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# id でユーザーを取得（認証後のユーザー情報取得で使用）
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
