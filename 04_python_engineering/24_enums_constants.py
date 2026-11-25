"""Objective: Learn how to define fixed sets of allowed values using Enum and 
how to manage constants in Python."""

"""

from enum import Enum

# Constants
COMPANY_NAME = "ABC Technologies"
MAX_EMPLOYEES = 100
MINIMUM_AGE = 18


# Define an Enum
class Department(Enum):
    HR = "Human Resources"
    IT = "Information Technology"
    FINANCE = "Finance"
    SALES = "Sales"


# Employee class
class Employee:

    def __init__(self, name, department):
        self.name = name
        self.department = department

    def display_details(self):
        print(f"Company: {COMPANY_NAME}")
        print(f"Employee: {self.name}")
        print(f"Department: {self.department.value}")


# Create employees
emp1 = Employee("Rahul", Department.IT)
emp2 = Employee("Priya", Department.HR)

emp1.display_details()
print()

emp2.display_details()

print(Department.IT)
print(Department.IT.name)
print(Department.IT.value)


def assign_department(department_name: str):
    try:
        department = Department[department_name]
        print(f"Assigned department: {department.value}")

    except KeyError:
        print("Invalid department!")

assign_department("IT")
assign_department("Finance")
"""
"""
Remember: Department[name] looks up by name; Department(value) looks up by value.
"""
"""
Department.IT
IT
Information Technology
"""

#------- with pydantic----

"""
from enum import Enum
from pydantic import BaseModel

# Constants stay the same in Python
COMPANY_NAME = "ABC Technologies"
MAX_EMPLOYEES = 100
MINIMUM_AGE = 18


# Inheriting from (str, Enum) lets Pydantic accept raw strings like "Finance"
class Department(str, Enum):
    HR = "Human Resources"
    IT = "Information Technology"
    FINANCE = "Finance"
    SALES = "Sales"


# BaseModel automatically generates __init__, type checking, and serialization
class Employee(BaseModel):
    name: str
    department: Department

    def display_details(self):
        print(f"Company: {COMPANY_NAME}")
        print(f"Employee: {self.name}")
        print(f"Department: {self.department.value}")


# 1. Works with the Enum member (just like before)
emp1 = Employee(name="Rahul", department=Department.IT)

# 2. ALSO works with a plain string! Pydantic converts it automatically
emp2 = Employee(name="Priya", department="Human Resources")

emp1.display_details()
print()
emp2.display_details()

"""
"""
Important distinction
You can retrieve an Enum member in two ways:
Department.IT



Using its member name.
Department("Information Technology")



Using its value.

But this will raise a ValueError:
Department("IT")



Because "IT" is the member's name, not its value.
"""
#--------------------
"""
We've learned how Enums work for employee departments. Now let's apply them to employee status.
Step 8: Create an Employee Status Enum
In a real employee management system, an employee can have different statuses:
- Active
- Inactive
- On leave
We don't want developers entering arbitrary values such as "Working", "Available" or "OnLeave".
1. Add a new Enum
Below your existing Department class, add:
"""
"""
from enum import Enum

# Constants
COMPANY_NAME = "ABC Technologies"
MAX_EMPLOYEES = 100
MINIMUM_AGE = 18


# Define an Enum
class Department(Enum):
    HR = "Human Resources"
    IT = "Information Technology"
    FINANCE = "Finance"
    SALES = "Sales"

class EmployeeStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ON_LEAVE = "On Leave"

# Employee class
class Employee:

    def __init__(self, name, department, status=EmployeeStatus.ACTIVE):
        self.name = name
        self.department = department
        self.status = status

    def display_details(self):
        print(f"Company: {COMPANY_NAME}")
        print(f"Employee: {self.name}")
        print(f"Department: {self.department.value}")
        print(f"Status: {self.status.value}")


# Create employees
emp1 = Employee("Rahul", Department.IT)

emp2 = Employee(
    "Priya",
    Department.HR,
    EmployeeStatus.ON_LEAVE
)

emp3 = Employee(
    "Amit",
    Department.FINANCE,
    EmployeeStatus.INACTIVE
)

emp1.display_details()
print()

emp2.display_details()
print()

emp3.display_details()

emp1.display_details()
print()

emp2.display_details()

print(Department.IT)
print(Department.IT.name)
print(Department.IT.value)


def assign_department(department_name: str):
    try:
        department = Department[department_name]
        print(f"Assigned department: {department.value}")

    except KeyError:
        print("Invalid department!")

assign_department("IT")
assign_department("Finance")

"""

from enum import Enum, auto


# ==========================================
# 1. CONSTANTS
# ==========================================

COMPANY_NAME = "ABC Technologies"
MAX_EMPLOYEES = 100
MINIMUM_AGE = 18


# ==========================================
# 2. DEPARTMENT ENUM
# ==========================================

class Department(Enum):
    HR = "Human Resources"
    IT = "Information Technology"
    FINANCE = "Finance"
    SALES = "Sales"


# ==========================================
# 3. EMPLOYEE STATUS ENUM
# ==========================================

class EmployeeStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ON_LEAVE = "On Leave"


# ==========================================
# 4. TASK STATUS ENUM USING AUTO()
# ==========================================

class TaskStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


# ==========================================
# 5. EMPLOYEE CLASS
# ==========================================

class Employee:

    def __init__(
        self,
        name,
        department,
        status=EmployeeStatus.ACTIVE
    ):
        self.name = name
        self.department = department
        self.status = status

    def display_details(self):
        print(f"Company: {COMPANY_NAME}")
        print(f"Employee: {self.name}")
        print(f"Department: {self.department.value}")
        print(f"Status: {self.status.value}")


# ==========================================
# 6. CREATE EMPLOYEES
# ==========================================

emp1 = Employee("Rahul", Department.IT)

emp2 = Employee(
    "Priya",
    Department.HR,
    EmployeeStatus.ON_LEAVE
)

emp3 = Employee(
    "Amit",
    Department.FINANCE,
    EmployeeStatus.INACTIVE
)

print("\n--- EMPLOYEE DETAILS ---")

emp1.display_details()
print()

emp2.display_details()
print()

emp3.display_details()


# ==========================================
# 7. ENUM NAME AND VALUE
# ==========================================

print("\n--- ENUM NAME AND VALUE ---")

department = Department.IT

print(department)
print(department.name)
print(department.value)


# ==========================================
# 8. VALIDATE DEPARTMENT USING ENUM
# ==========================================

def assign_department(department_name: str):

    try:
        department = Department(department_name)
        print(f"Assigned department: {department.name}")

    except ValueError:
        print("Invalid department!")


print("\n--- DEPARTMENT VALIDATION ---")

assign_department("Information Technology")
assign_department("Finance")
assign_department("Marketing")


# ==========================================
# 9. LOOKUP ENUM USING MEMBER NAME
# ==========================================

def assign_department_by_name(department_name: str):

    try:
        department = Department[department_name]
        print(f"Assigned department: {department.value}")

    except KeyError:
        print("Invalid department!")


print("\n--- DEPARTMENT LOOKUP BY NAME ---")

assign_department_by_name("IT")
assign_department_by_name("FINANCE")
assign_department_by_name("Finance")


# ==========================================
# 10. CONSTANT-BASED VALIDATION
# ==========================================

def can_hire(age: int):

    if age < MINIMUM_AGE:
        return False

    return True


print("\n--- AGE VALIDATION ---")

print(can_hire(17))
print(can_hire(25))


# ==========================================
# 11. ENUM COMPARISON: IS VS ==
# ==========================================

print("\n--- ENUM COMPARISON ---")

status1 = EmployeeStatus.ACTIVE
status2 = EmployeeStatus.ACTIVE
status3 = EmployeeStatus.INACTIVE

print(status1 == status2)
print(status1 is status2)
print(status1 == status3)


# ==========================================
# 12. ITERATE THROUGH ENUM
# ==========================================

print("\n--- ALL EMPLOYEE STATUSES ---")

for status in EmployeeStatus:
    print(status.name, status.value)


# ==========================================
# 13. CONVERT ENUM INTO LIST
# ==========================================

print("\n--- ENUM LIST ---")

status_list = list(EmployeeStatus)

print(status_list)


# Get only the values

status_values = [
    status.value for status in EmployeeStatus
]

print(status_values)


# ==========================================
# 14. CHECK WHETHER A VALUE EXISTS
# ==========================================

def is_valid_status(value: str):

    return value in [
        status.value for status in EmployeeStatus
    ]


print("\n--- STATUS VALIDATION ---")

print(is_valid_status("Active"))
print(is_valid_status("Working"))


# ==========================================
# 15. TASK STATUS USING AUTO()
# ==========================================

print("\n--- TASK STATUS VALUES ---")

for task in TaskStatus:
    print(task.name, task.value)

"""
2. Use IntEnum
Python also provides IntEnum.

Add:
from enum import IntEnumclass Priority(IntEnum):    LOW = 1    MEDIUM = 2    HIGH = 3



The important difference is that IntEnum members can be compared with ordinary integers.
"""
from enum import IntEnum
class Priority(IntEnum):    
    LOW = 1    
    MEDIUM = 2    
    HIGH = 3
print(Priority.HIGH == 3)
print(Priority.HIGH > Priority.LOW)
print(Priority.MEDIUM + 1)
#With ordinary Enum, these integer comparisons and arithmetic operations aren't supported in the same way.
# by normal Enum
"""
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


# Must use .value for comparisons and arithmetic
print(Priority.HIGH.value == 3)  # True
print(Priority.HIGH.value > Priority.LOW.value)  # True
print(Priority.MEDIUM.value + 1)  # 3

"""
from enum import StrEnum

class OrderStatus(StrEnum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

print(OrderStatus.SHIPPED == "shipped")
print(OrderStatus.SHIPPED.upper())
print(str(OrderStatus.SHIPPED))

print("\n--- PRIORITY COMPARISON ---")

if Priority.HIGH > Priority.MEDIUM:
    print("High priority task")

print("\n--- ORDER STATUS ---")

if OrderStatus.SHIPPED == "shipped":
    print("Order has been shipped")

print(OrderStatus.SHIPPED)