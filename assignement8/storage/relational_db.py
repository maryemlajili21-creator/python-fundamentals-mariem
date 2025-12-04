from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from assignement8.models.relational import Base

DATABASE_URL = "mysql+pymysql://root:mariem@localhost/arxiv_db"

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
Session = sessionmaker(bind=engine)


def create_all() -> None:
    """Create all tables in the database."""
    Base.metadata.create_all(engine)
