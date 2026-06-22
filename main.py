from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from schemas import EmployeeCreate, EmployeeUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend.html
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Employee Management API Running"
    }


@app.post("/employees")
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    new_employee = models.Employee(
        name=employee.name,
        department=employee.department,
        salary=employee.salary
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@app.get("/employees")
def get_employees(
    db: Session = Depends(get_db)
):
    return db.query(models.Employee).all()


@app.get("/employees/{emp_id}")
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == emp_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@app.put("/employees/{emp_id}")
def update_employee(
    emp_id: int,
    updated_employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == emp_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee.name = updated_employee.name
    employee.department = updated_employee.department
    employee.salary = updated_employee.salary

    db.commit()
    db.refresh(employee)

    return employee


@app.delete("/employees/{emp_id}")
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == emp_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }


@app.get("/search")
def search_employee(
    department: str,
    db: Session = Depends(get_db)
):
    employees = db.query(models.Employee).filter(
        models.Employee.department == department
    ).all()

    return employees