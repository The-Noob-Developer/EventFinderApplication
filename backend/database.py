from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://sql12785962:8TAN7uFLsr@sql12.freesqldatabase.com:3306/sql12785962"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()