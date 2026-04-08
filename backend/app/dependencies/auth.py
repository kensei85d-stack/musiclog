from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.app.core.security import decode_access_token

# Swagger の "Authorize" と連携する設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT から user_id を取り出す（認証必須 API で使用）
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return int(payload["sub"])
