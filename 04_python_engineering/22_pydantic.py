"""
Pydantic is especially useful in your Applied AI and FastAPI projects. 
It helps ensure that incoming API data has the correct structure and data types.
"""


from pydantic import BaseModel, ValidationError


class Employee(BaseModel):
    name: str
    age: int
    salary: float
    is_active: bool


employee_data = {
    "name": "Rahul",
    "age": 30,
    "salary": 55000,
    "is_active": True
}

employee = Employee(**employee_data)

print(employee)
print(employee.name)
print(employee.age)
print(type(employee.salary))
