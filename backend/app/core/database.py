from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.core.config import settings

# Base クラス（モデルが継承する）
Base = declarative_base()

# SQLAlchemy エンジン（遅延初期化）
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.DATABASE_URL,
            echo=False,
            future=True
        )
    return _engine

# セッション
def get_session():
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine()
    )
    return SessionLocal

# FastAPI の Depends 用
def get_db():
    SessionLocal = get_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()