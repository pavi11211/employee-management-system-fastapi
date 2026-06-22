from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    name:str
    department:str
    salary:int

class EmployeeUpdate(BaseModel):
    name:str
    department:str
    salary:int

class EmployeeResponse(BaseModel):
    id:int
    name:str
    department:str
    salary:int