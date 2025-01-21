from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd
from operations import create_departments, create_jobs, create_employees, get_employees_by_quarter, get_departments_average
from database import get_db

app = FastAPI()

@app.get("/", tags=['Home'])
def home():
    """
    Endpoint principal que devuelve un mensaje de bienvenida.

    Este endpoint está destinado para ser la página de inicio de la API.

    Returns:
        str: Mensaje de bienvenida al API.
    """
    return "Bienvenido al API"

@app.post("/upload/departments", tags=['Upload'])
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Carga un archivo CSV que contiene los departamentos y lo guarda en la base de datos en la tabla `departments`.

    El archivo CSV debe tener al menos dos columnas: 
        'id' (identificador del departamento) 
        'depto' (nombre del departamento). Los datos serán insertados .

    Args:
        file (UploadFile): El archivo CSV que contiene los datos de los departamentos.
        db (Session): La sesión de la base de datos que se inyecta automáticamente por FastAPI.

    Returns:
        dict: Mensaje de éxito indicando que los departamentos se han cargado correctamente.
    """
    # Leer datos del CSV
    data = pd.read_csv(file.file, delimiter=',',index_col=False, header=None,names=['id', 'depto'])
    # Cargar departamentos
    create_departments(db, data)

    return {"message": "CSV departments uploaded successfully!"}

@app.post("/upload/jobs", tags=['Upload'])
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Carga un archivo CSV que contiene los trabajos y los guarda en la base de datos en la tabla de `jobs`.

    El archivo CSV debe tener al menos dos columnas: 
        'id' (identificador del trabajo) 
        'job' (nombre del trabajo).

    Args:
        file (UploadFile): El archivo CSV que contiene los datos de los trabajos.
        db (Session): La sesión de la base de datos que se inyecta automáticamente por FastAPI.

    Returns:
        dict: Mensaje de éxito indicando que los trabajos se han cargado correctamente.
    """
    # Leer datos del CSV
    jobs = pd.read_csv(file.file, delimiter=',',index_col=False, header=None,names=['id', 'job'])
    # Cargar datos
    create_jobs(db, jobs)

    return {"message": "CSV jobs: uploaded successfully!"}

@app.post("/upload/employees", tags=['Upload'])
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Carga un archivo CSV que contiene los empleados y los guarda en la base de datos en la tabla `employees`.

    El archivo CSV debe tener cinco columnas: 
        'id' (identificador del empleado), 
        'name' (nombre del empleado), 
        'datetime' (fecha de contratación), 
        'department_id' (identificador del departamento) 
        'job_id' (identificador del trabajo).
    
    Los valores NaN se reemplazan por 0 en las columnas 'department_id' y 'job_id'.

    Args:
        file (UploadFile): El archivo CSV que contiene los datos de los empleados.
        db (Session): La sesión de la base de datos que se inyecta automáticamente por FastAPI.

    Returns:
        dict: Mensaje de éxito indicando que los empleados se han cargado correctamente.
    """
    # Leer datos del CSV
    employees = pd.read_csv(
        file.file, 
        delimiter=',',
        index_col=False, 
        header=None,
        names=['id', 'name','datetime','department_id','job_id'], 
        na_values=['Unknown','NaN']
        )

    # Llenar valores nulos
    employees['department_id'] = employees['department_id'].fillna(0)
    employees['job_id'] = employees['job_id'].fillna(0)
    # Convertir a enteros
    employees['department_id'] = employees['department_id'].astype(int)
    employees['job_id'] = employees['job_id'].astype(int)
    # Cargar datos
    create_employees(db, employees)

    return {"message": "CSV employees: uploaded successfully!"}

@app.get("/employees", tags=['Query'])
def get_employees_quarter(db: Session = Depends(get_db)):
    """
    Número de empleados contratados para cada puesto y departamento en 2021 dividido por trimestre. 
    La respuesta esta ordenada alfabéticamente por departamento y puesto.

    Args:
        db (Session): La sesión de la base de datos que se inyecta automáticamente por FastAPI.

    Returns:
        list: Una lista de diccionarios que contienen los datos del departamento, trabajo y la cantidad de empleados contratados
              en cada trimestre (Q1, Q2, Q3, Q4).
    """
    data = get_employees_by_quarter(db)
    response = []
    for department, job, q1, q2, q3, q4 in data:
        response.append({
            "department": department,
            "job": job,
            "Q1": int(q1) if q1 else 0,
            "Q2": int(q2) if q2 else 0,
            "Q3": int(q3) if q3 else 0,
            "Q4": int(q4) if q4 else 0,
        })
    return response

@app.get("/departments", tags=['Query'])
def get_department(db: Session = Depends(get_db)):
    """
    Lista de ids, nombre y número de empleados contratados de cada departamento que contrató más 
    empleados que la media de empleados contratados en 2021 para todos los departamentos, 
    ordenados por el número de empleados contratados (descendente).

    Args:
        db (Session): La sesión de la base de datos que se inyecta automáticamente por FastAPI.

    Returns:
        list: Una lista de diccionarios que contienen el id, nombre y cantidad de empleados contratados por cada departamento.
    """
    data = get_departments_average(db)
    response = [
        {"id": department_id, "department": department_name, "hired": hired}
        for department_id, department_name, hired in data
    ]
    return response
