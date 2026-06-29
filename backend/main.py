from fastapi import FastAPI

# ルーター読み込み
from backend.app.routers import auth, history, stats

app = FastAPI(
    title="MusicLog API",
    version="1.0.0"
)

# ルーター登録
app.include_router(auth.router, tags=["auth"])
app.include_router(history.router, tags=["history"])
app.include_router(stats.router, tags=["stats"])

@app.get("/")
def root():
    return {"message": "MusicLog API is running"}