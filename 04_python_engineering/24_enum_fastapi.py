"""
Imagine your employee API accepts a department from the user.

Without Enum, someone could submit "Marketing", "IIT" or "Accounts" even if those departments aren't supported.

We'll restrict the accepted values.
"""

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Employee Enum API")


# Define allowed departments
class Department(str, Enum):
    HR = "HR"
    IT = "IT"
    FINANCE = "FINANCE"
    SALES = "SALES"


# Define allowed employee statuses
class EmployeeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ON_LEAVE = "ON_LEAVE"


# Request model
class EmployeeCreate(BaseModel):
    name: str
    department: Department
    status: EmployeeStatus = EmployeeStatus.ACTIVE


@app.post("/employees")
def create_employee(employee: EmployeeCreate):

    return {
        "name": employee.name,
        "department": employee.department.value,
        "status": employee.status.value
    }


@app.get("/departments")
def get_departments():

    return [department.value for department in Department]
