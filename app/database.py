from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from .config import settings

print("DB URL:", settings.db_url)


engine = create_engine(settings.db_url)

def get_db():
    db = Session(bind=engine, autoflush=False, autocommit=False)
    try:
        yield db
    finally:
        db.close()
