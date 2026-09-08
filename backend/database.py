from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings


def utcnow_naive() -> datetime:
    """Current UTC time as a naive datetime, for naive DateTime columns.

    Replaces the deprecated datetime.utcnow() while keeping the same
    naive-UTC value the columns already store and compare against.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)

connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
