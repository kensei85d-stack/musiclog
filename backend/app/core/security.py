from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.core.config import settings

# パスワードハッシュ設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 設定（.env → settings から読み込み）
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# パスワードをハッシュ化
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# パスワードを検証
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT を作成
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


# JWT をデコード（失敗時は空 dict）
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return {}

# リフレッシュトークン（有効期限は長め）
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 日間

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    return create_access_token(
        data,
        expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )
