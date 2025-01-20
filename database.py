from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://user:password@host:port/databasename?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
