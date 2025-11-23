from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SessionType, sessionmaker

from models.relational import Base

DATABASE_URL = "mysql+pymysql://articles_user:articles_pass@localhost:3306/articles_db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, class_=SessionType)


def get_session() -> SessionType:
    """Create and return a new SQLAlchemy session."""
    return SessionLocal()


def init_db() -> None:
    """Create tables in MariaDB if they do not exist."""
    Base.metadata.create_all(engine)
