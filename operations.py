from sqlalchemy import func, case
from sqlalchemy.orm import Session
from models import Department, Job, Employee

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
    result = db.query(
        Department.department,
        Job.job,
        func.sum(
            case(
                (func.extract('quarter', Employee.datetime_) == 1, 1),  # Condición para Q1
                else_=0
            )
        ).label("Q1"),
        func.sum(
            case(
                (func.extract('quarter', Employee.datetime_) == 2, 1),  # Condición para Q2
                else_=0
            )
        ).label("Q2"),
        func.sum(
            case(
                (func.extract('quarter', Employee.datetime_) == 3, 1),  # Condición para Q3
                else_=0
            )
        ).label("Q3"),
        func.sum(
            case(
                (func.extract('quarter', Employee.datetime_) == 4, 1),  # Condición para Q4
                else_=0
            )
        ).label("Q4")
    ).join(
        Employee, Employee.department_id == Department.id
    ).join(
        Job, Employee.job_id == Job.id
    ).filter(
        func.extract('year', Employee.datetime_) == 2021
    ).group_by(
        Department.department, Job.job
    ).order_by(
        Department.department, Job.job
    ).all()

    return result

def get_departments_average(db: Session):
    count_employees = (
        db.query(
            Employee.department_id, 
            func.count(Employee.id).label("cont")
            )
        .join(Department, Employee.department_id==Department.id)
        .filter(func.extract("year", Employee.datetime_) == 2021)
        .group_by(Employee.department_id)
        .subquery()
    )

    average = (
        db.query(
            func.avg(count_employees.c.cont).label("average")
            )
        .scalar_subquery()
    )

    result = (
        db.query(
            Department.id,
            Department.department,
            func.count(Employee.id).label("hired")
        )
        .join(Employee, Employee.department_id == Department.id)
        .filter(func.extract("year", Employee.datetime_) == 2021)
        .group_by(Department.id)
        .having(func.count(Employee.id) > average)
        .order_by(func.count(Employee.id).desc())
        .all()
    )

    return result