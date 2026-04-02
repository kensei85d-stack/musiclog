from sqlalchemy import create_engine, text
from backend.app.core.config import settings

print('DATABASE_URL:', settings.DATABASE_URL)
engine = create_engine(settings.DATABASE_URL, future=True)
with engine.connect() as conn:
    print(conn.execute(text('select current_user, current_database()')).all())
