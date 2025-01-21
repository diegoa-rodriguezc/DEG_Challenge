from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Department(Base):
    """
    Tabla de departamentos

    Atributos:
        id (int): Identificador único.
        department (str): Nombre Departamento.
    """
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=False, autoincrement=False)
    department = Column(String, index=False)

    def __init__(self, id, department):
        self.id = id
        self.department = department

class Job(Base):
    """
    Tabla de trabajos

    Atributos:
        id (int): Identificador único.
        job (str): Nombre trabajo.
    """
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    job = Column(String, index=False)

    def __init__(self, id, job):
        self.id = id
        self.job = job

class Employee(Base):
    """
    Tabla de empleados

    Atributos:
        id (int): Identificador único.
        name (str): Nombre y Apellido del empleado.
        datetime_ (datetime): Fecha y hora de contratación.
        department_id (int): Identificador del departamento al que pertenece el empleado.
        job_id (int): Identificador del trabajo asignado al empleado.
    """
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    name = Column(String, index=False)
    datetime_ = Column(DateTime, index=False)
    department_id = Column(Integer, index=False)
    job_id = Column(Integer, index=False)

    def __init__(self, id, name, datetime_, department_id, job_id):
        self.id = id
        self.name = name
        self.datetime_ = self.convert_to_datetime(datetime_)
        self.department_id = department_id
        self.job_id = job_id

    @staticmethod
    def from_iso_format(datetime_str):
        """Convierte un string en formato ISO 8601 a un objeto datetime."""
        if isinstance(datetime_str, str):
            try:
                # Quitar el 'Z' al final si está presente
                datetime_str = datetime_str.rstrip('Z')
                return datetime.fromisoformat(datetime_str)
            except ValueError:
                return None  # Si no se puede convertir, retornamos None
        return None  # Si no es una cadena, retornamos None

    @staticmethod
    def convert_to_datetime(datetime_str):
        """Convierte una cadena a datetime solo si es válida."""
        if datetime_str and datetime_str != "NaN":  # Validación de "NaN" y valores inválidos
            return Employee.from_iso_format(datetime_str)
        return None  # Si la fecha no es válida o no es una cadena, retornamos None