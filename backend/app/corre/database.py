from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# SQLAlchemy エンジン
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# セッション
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base クラス（モデルが継承する）
Base = declarative_base()

# FastAPI の Depends 用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()