from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de Base de datos

# Cadena de conexión a una Base de datos MS SQL Server (reemplazar los valores según corresponda)
#SQLALCHEMY_DATABASE_URL = ("mssql+pyodbc://user:password@host:ip/databasename?driver=ODBC+Driver+17+for+SQL+Server")

# Cadena de conexión a una Base de datos PostgreSQL (reemplazar los valores según corresponda)
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/databasename"

engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Devuelve una sesión de base de datos.

    Returns:
        Session: Una instancia de sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as error:
        print('ERROR', error)
        raise
    finally:
        db.close()
