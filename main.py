from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd
from operations import create_departments, create_jobs, create_employees, get_employees,get_employees_by_quarter
from database import get_db

app = FastAPI()

@app.get("/", tags=['Home'])
def home():
    return "Bienvenido al API"

@app.post("/upload/departments", tags=['Upload'])
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = pd.read_csv(file.file, delimiter=',',index_col=False, header=None,names=['id', 'depto'])
    # Cargar departamentos
    create_departments(db, data)

    return {"message": "CSV uploaded successfully!"}

@app.post("/upload/jobs", tags=['Upload'])
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    jobs = pd.read_csv(file.file, delimiter=',',index_col=False, header=None,names=['id', 'job'])
    create_jobs(db, jobs)

    return {"message": "CSV jobs: uploaded successfully!"}

@app.post("/upload/employees", tags=['Upload'])
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    employees = pd.read_csv(
        file.file, 
        delimiter=',',
        index_col=False, 
        header=None,
        names=['id', 'name','datetime','department_id','job_id'], 
        na_values=['Unknown']
        )
    employees['department_id'] = employees['department_id'].fillna(0)
    employees['job_id'] = employees['job_id'].fillna(0)

    employees['department_id'] = employees['department_id'].astype(int)
    employees['job_id'] = employees['job_id'].astype(int)
    create_employees(db, employees)

    return {"message": "CSV employees: uploaded successfully!"}

@app.get("/employees", tags=['Query'])
def query_employees(db: Session = Depends(get_db)):
    result = get_employees_by_quarter(db)
    return result
