from sqlalchemy.orm import Session
import pandas as pd
from models import Department, Job, Employee
from datetime import datetime

def create_departments(db: Session, departments_data: list):
    departments = [Department(id=id,department=dep) for id,dep in departments_data.itertuples(index=False, name=None)]
    db.add_all(departments)
    db.commit()

def create_jobs(db: Session, jobs_data: list):
    jobs = [Job(id=id,job=job) for id,job in jobs_data.itertuples(index=False, name=None)]
    db.add_all(jobs)
    db.commit()

def create_employees(db: Session, employees_data: list):
    employees = [Employee(id=id,name=name,datetime_=datetime,department_id=department_id,job_id=job_id) for id,name,datetime,department_id,job_id in employees_data.itertuples(index=False, name=None)]
    db.add_all(employees)
    db.commit()

def get_employees(db: Session):
    employees = db.query(Employee)
    return employees



def get_employees_by_quarter(db: Session):
    # Filtrar los empleados contratados en 2021
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 12, 31)
    
    employees = db.query(Employee).filter(Employee.datetime_ >= start_date, Employee.datetime_ <= end_date).all()

    # Crear un DataFrame de pandas
    data = []
    for emp in employees:
        department_name = emp.department.department
        job_name = emp.job.job
        hire_date = emp.datetime_

        # Identificar el trimestre en el que fue contratado el empleado
        if hire_date.month in [1, 2, 3]:
            quarter = 'Q1'
        elif hire_date.month in [4, 5, 6]:
            quarter = 'Q2'
        elif hire_date.month in [7, 8, 9]:
            quarter = 'Q3'
        else:
            quarter = 'Q4'
        
        data.append([department_name, job_name, quarter])
    
    df = pd.DataFrame(data, columns=['department', 'job', 'quarter'])
    
    # Obtener el número de empleados por departamento, trabajo y trimestre
    result = df.groupby(['department', 'job', 'quarter']).size().unstack(fill_value=0)
    
    # Ordenar el resultado alfabéticamente por departamento y trabajo
    result = result.sort_index(axis=0).sort_index(axis=1)
    
    # Convertir el resultado a formato diccionario para la respuesta de la API
    result_dict = result.to_dict(orient='index')
    
    return result_dict
