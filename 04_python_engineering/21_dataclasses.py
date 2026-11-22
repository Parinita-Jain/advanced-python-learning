"""
Objective: Learn how to create structured data objects without writing repetitive __init__(), __repr__() 
and comparison methods manually.

Dataclasses are particularly useful when building applications that handle employees, customers, 
API requests, configurations and other structured records.
"""
"""
Instead of writing a class with an __init__() method, we can use the @dataclass decorator to automatically generate it for us.


class Employee:

    def __init__(self, employee_id, name, salary, department):
        self.employee_id = employee_id
        self.name = name
        self.salary = salary
        self.department = department


emp1 = Employee(101, "Rahul", 50000, "IT")

print(emp1.name)

You have to manually write the constructor and assign every attribute.

Now let's achieve the same thing using a dataclass.

"""


from dataclasses import dataclass


@dataclass
class Employee:

    employee_id: int
    name: str
    salary: float
    department: str


emp1 = Employee(101, "Rahul", 50000, "IT")

print(emp1)
print(emp1.name)
print(emp1.salary)

"""
Notice that Python automatically generated:
- __init__() — initializes attributes.
- __repr__() — provides a readable object representation.
- __eq__() — compares objects by their fields.
4. Understanding default values and field()
Suppose some employees belong to the IT department while others belong to HR.

You can provide default values:
"""


from dataclasses import dataclass, field


@dataclass
class Employee:

    employee_id: int
    name: str
    salary: float
    department: str = "IT"
    skills: list[str] = field(default_factory=list)


emp1 = Employee(101, "Rahul", 50000)
emp2 = Employee(102, "Priya", 60000, "HR")

emp1.skills.append("Python")

print(emp1)
print(emp2)

"""
Why default_factory=list?

It creates a fresh list for every employee.

Avoid using:

skills: list[str] = []

Dataclasses reject mutable defaults like this because sharing one list between instances would be unsafe.
5. Immutable dataclasses — frozen=True
Sometimes you want to prevent an object's attributes from being modified after creation.
"""
"""
@dataclass(frozen=True)
class EmployeeID:

    employee_id: int
    name: str


emp = EmployeeID(101, "Rahul")

emp.name = "Priya"
"""
"""
The last line raises:
dataclasses.FrozenInstanceError


This is useful for records that should not be modified after creation.
6. Converting dataclasses into dictionaries
Python provides asdict().
"""
from dataclasses import asdict

employee = Employee(101, "Rahul", 50000)

employee_dict = asdict(employee)

print(employee_dict)

"""
This is particularly useful when preparing structured data for JSON serialization or APIs.

Another useful function is replace():
"""

from dataclasses import replace

updated_employee = replace(employee, salary=60000)

print(updated_employee)
print(employee)

#It creates a new dataclass object with the specified changes. The original object remains unchanged.