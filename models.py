from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=False, autoincrement=False)
    department = Column(String, index=False)

    def __init__(self, id, department):
        self.id = id
        self.department = department

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    job = Column(String, index=False)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    name = Column(String, index=False)
    datetime_ = Column(String, index=False)
    department_id = Column(Integer, index=False)
    job_id = Column(Integer, index=False)

