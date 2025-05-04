from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DB_URL = 'sqlite:///bookstore.db'

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()


def create_connection():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
