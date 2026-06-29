import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

from backend.app.core.config import settings

# Import the correct Base from backend app
from backend.app.core.database import Base

# Import all models to register them
from backend.app.models.user import User
from backend.app.models.artist import Artist
from backend.app.models.track import Track
from backend.app.models.Play_history import PlayHistory

target_metadata = Base.metadata

config = context.config

# Use the app settings value if available (keeps Alembic in sync with application)
DB_URL = settings.DATABASE_URL

def run_migrations_offline():
    url = DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url = DB_URL
    print("ALEMBIC DB URL:", url) 
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
