from fastapi import FastAPI
from app.routers import auth, history, stats  # 後で作る

app = FastAPI(
    title="MusicLog API",
    version="1.0.0"
)

# ルーター登録（後で実装）
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(history.router, prefix="/history", tags=["history"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

@app.get("/")
def root():
    return {"message": "MusicLog API is running"}