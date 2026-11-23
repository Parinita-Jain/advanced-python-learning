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

"""
We've covered:
1. Basic Pydantic models and validation.
2. Automatic type conversion (coercion).
3. Strict validation using ConfigDict(strict=True).
4. Field constraints using Field().
5. Optional fields and default values.
"""

"""
1. Why do we need nested models?
Consider an employee API receiving this JSON:

{
    "name": "Rahul",
    "age": 30,
    "address": {
        "city": "Mumbai",
        "pincode": 400001
    },
    "skills": ["Python", "SQL", "Machine Learning"]
}

Notice that address is itself an object inside the employee object.

We need to validate both the employee information and the address information.

Pydantic supports this through nested models.

"""


from pydantic import BaseModel, Field


class Address(BaseModel):
    city: str
    pincode: int


class Employee(BaseModel):
    name: str
    age: int = Field(ge=18, le=60)
    address: Address
    skills: list[str]


employee_data = {
    "name": "Rahul",
    "age": 30,
    "address": {
        "city": "Mumbai",
        "pincode": 400001
    },
    "skills": ["Python", "SQL", "Machine Learning"]
}

employee = Employee(**employee_data)

print(employee)
print(employee.address.city)
print(employee.skills[0])

"""
Automatic nested parsing
employee = Employee(**employee_data)

Even though employee_data["address"] is a Python dictionary, 
Pydantic automatically converts it into an Address object and validates its fields.

Pydantic can convert the numeric string into an integer.

"""
#--------------------
"""
Part 4: Custom Validators
Now let's learn how to write our own validation rules.

For example, suppose employee names must contain only alphabetic characters and spaces.

Pydantic provides @field_validator for this.
"""
"""
from pydantic import BaseModel, field_validator, ValidationError


class Employee(BaseModel):
    name: str
    age: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")

        return value


emp1 = Employee(name="Rahul Sharma", age=30)
print(emp1)

emp2 = Employee(name="Rahul123", age=30)
print(emp2)

"""
"""
As you saw in your Employee validation code, Pydantic checks whether "Rahul123" is valid before creating the Employee object. 
Since the object doesn't exist yet, 
Pydantic runs the check as a @classmethod on the blueprint.
"""

"""
Step 2: Understand the decorator
@field_validator("name")



This tells Pydantic to execute the custom validation function whenever the name field is validated.
@classmethod
def validate_name(cls, value):



- cls refers to the Employee model.
- value contains the incoming name.
- raise ValueError() signals invalid data.
- return value returns the validated value.
Step 3: Expected behaviour
- Rahul Sharma → accepted.
- Rahul123 → rejected with ValidationError.
"""
"""
Project 22 – Part 6: Model Validators
So far, @field_validator has validated individual fields.

But what if validation depends on two or more fields together?

Example: An employee's joining date and leaving date. The leaving date must be later than the joining date.

Pydantic provides @model_validator for this.
Step 1: Add this code
"""
from datetime import date
from pydantic import BaseModel, model_validator


class Employee(BaseModel):
    name: str
    joining_date: date
    leaving_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.leaving_date <= self.joining_date:
            raise ValueError("Leaving date must be after joining date")

        return self
emp = Employee(
    name="Rahul",
    joining_date="2024-01-10",
    leaving_date="2025-01-10"
)

print(emp)


"""

Validator Decorator	When It Runs	Uses @classmethod?	First Argument	What It Returns
@field_validator(...)	Before the model is built (per field)	Yes	cls	The validated field value
@model_validator(mode="before")	Before the model is built (raw input dict)	Yes	cls	The raw dictionary/data
@model_validator(mode="after")	After the model is built	No (normal method)	self	self (the model instance)

"""

"""
Step 2: Understand the difference
Validator	Purpose
@field_validator	Validates an individual field
@model_validator	Validates the model as a whole, often using multiple fields

Notice:
@model_validator(mode="after")



- after means validation runs after the model's fields have been parsed.
- self gives access to the validated model fields.
- We return self when validation succeeds.
"""

from pydantic import BaseModel, field_validator


class Employee(BaseModel):
    salary: float

    @field_validator("salary")
    @classmethod
    def validate_salary(cls, value):
        if value < 30000:
            raise ValueError("Salary must be at least 30000")

        return value
"""
Note that this rule could also be implemented more simply using Field(ge=30000). 
Custom validators are useful when the validation logic is more complex.
"""
"""
Pydantic: Progress
We've covered:
1. Basic models and type validation.
2. Type coercion and strict mode.
3. Field constraints.
4. Optional fields.
5. Nested models.
6. Custom field validators.
7. Model validators.
"""
"""
Pydantic serialization
We'll learn:
- model_dump()
- model_dump_json()
- model_validate()
- model_validate_json()
These are particularly useful when exchanging data between FastAPI, databases and LLM applications.

Let's continue with serialization.
"""
"""
In real-world applications, we frequently need to convert Python objects into formats that APIs and databases can understand.

Pydantic provides two important methods:
- model_dump() – converts a Pydantic model into a Python dictionary.
- model_dump_json() – converts a Pydantic model into a JSON string.
"""
"""
A Pydantic model is any Python class you create that inherits from BaseModel—and yes, 
the objects created from that class (like emp = Employee(...)) are instances of that Pydantic model.
Think of it as a "smart data container" that automatically checks, cleans, and converts messy external data 
(like JSON from an API, form inputs, or CSV rows) into clean, reliable Python objects.
"""

from pydantic import BaseModel


class Employee(BaseModel):
    name: str
    age: int
    skills: list[str]


emp = Employee(
    name="Rahul",
    age=30,
    skills=["Python", "SQL", "Machine Learning"]
)

# Convert model into dictionary
employee_dict = emp.model_dump()

print(employee_dict)
print(type(employee_dict))

# Convert model into JSON string
employee_json = emp.model_dump_json()

print(employee_json)
print(type(employee_json))

"""
Step 3: Understand the difference
Method	Returns	Typical use
model_dump()	Python dictionary	Python application logic, database operations
model_dump_json()	JSON string	API communication, JSON storage

Remember: JSON is a string representation of structured data. It is not a Python dictionary.
"""
print(employee_dict["name"])
#print(employee_json["name"])
#The first statement works. The second raises an error because employee_json is a string, not a dictionary.

"""
1. Use employee_dict instead (Best if you already dumped a dict):python
print(employee_dict["name"])  # Output: Rahul
Use code with caution.
2. Access it directly on the Pydantic model emp (Cleanest):python
print(emp.name)  # Output: Rahul
Use code with caution.
3. If you ONLY have the employee_json string (e.g., received from an API or file):
Use Python's built-in json.loads() to convert the JSON string into a dictionary first:python
import json

parsed_data = json.loads(employee_json)
print(parsed_data["name"])  # Output: Rahul
Use code with caution.
(Or load it back into a Pydantic model with Employee.model_validate_json(employee_json).name.)

"""

"""
Part 8: Deserialization and Validation
Serialization converts a Pydantic object into a dictionary or JSON string.

Deserialization converts dictionary or JSON data back into a Pydantic object.

This code shows the reverse process (deserialization): taking raw external data—a Python dictionary (employee_data) 
and a raw JSON text string (employee_json)—and converting both into validated Employee Pydantic objects.
Step 1: Update your code
"""

from pydantic import BaseModel


class Employee(BaseModel):
    name: str
    age: int
    skills: list[str]


# Dictionary to Pydantic object
employee_data = {
    "name": "Rahul",
    "age": 30,
    "skills": ["Python", "SQL"]
}

emp1 = Employee.model_validate(employee_data)

print(emp1)
print(type(emp1))


# JSON string to Pydantic object
employee_json = '''
{
    "name": "Priya",
    "age": 28,
    "skills": ["Python", "Machine Learning"]
}
'''

emp2 = Employee.model_validate_json(employee_json)

print(emp2)
print(type(emp2))

"""
Step 2: Understand the methods
Method	Input	Output
model_dump()	Pydantic object	Dictionary
model_dump_json()	Pydantic object	JSON string
model_validate()	Dictionary or compatible Python object	Pydantic object
model_validate_json()	JSON string or bytes	Pydantic object

Both validation methods validate the incoming data against the model's schema.
"""

"""
1. emp1 = Employee.model_validate(employee_data)
	• Input: A regular Python dict (employee_data).
	• What it does: Checks that "name", "age", and "skills" exist and match the required types (str, int, list[str]), without needing **employee_data.
	• Output: Creates a real Employee object (emp1). You can now access fields cleanly using dot notation like emp1.name ("Rahul").
2. emp2 = Employee.model_validate_json(employee_json)
	• Input: A raw JSON string (employee_json, type str—the kind of text you receive from a web API or read from a .json file).
	• What it does: Parses the JSON text and validates all field types in one fast step (written in Rust under the hood in Pydantic v2). You don't need to call json.loads() manually first.
	• Output: Creates a real Employee object (emp2). You can now access emp2.name ("Priya") and emp2.skills.

The Complete Pydantic Data Lifecycle


Direction	From dict	From JSON str
Raw Data → Pydantic Model (Reading/Validating)	Employee.model_validate(data_dict)	Employee.model_validate_json(json_str)
Pydantic Model → Raw Data (Exporting/Sending)	emp.model_dump()	emp.model_dump_json()

"""

"""
Yes—Employee(**employee_data) does the exact same thing as Employee.model_validate(employee_data), 
and it also automatically validates the nested Address dictionary inside it.

"""
"""
Use Employee(**data) when you are manually constructing an object from a known dictionary in clean Python code, 
and use Employee.model_validate(data) when validating dynamic, unknown, or non-dictionary inputs (like database ORM objects or unverified API payloads).
When data is a standard Python dict, both give the exact same result—the choice comes down to readability, flexibility,
 and safety.
"""

"""
Part 9: Handling missing and extra fields
One important question when building APIs is: what happens if incoming data contains fields that 
aren't defined in our model?

Consider:
"""
from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    age: int

emp = Employee(
    name="Rahul",
    age=30,
    department="IT"
)

print(emp)

"""
By default, Pydantic's extra-field policy is ignore.

This means:
- name is accepted.
- age is accepted.
- department is silently ignored.
You can change this behaviour using ConfigDict.
Three extra-field policies
Policy	Behaviour
ignore	Ignores extra fields (default)
forbid	Raises ValidationError
allow	Accepts and retains extra fields

Experiment
Change the model to:
"""
"""
from pydantic import BaseModel, ConfigDict

class Employee(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    age: int

    Try creating the employee with department="IT" again.

You should get a ValidationError.

    
"""
from pydantic import BaseModel, ConfigDict

class Employee(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    age: int

emp = Employee(name="Rahul", age=30, department="IT")

print(emp.department)
print(emp.model_dump())

"""
Notice that department is not declared in the model, but Pydantic retains it.
Project 22 – Progress
We've now covered:
1. Basic models and type validation
2. Type coercion and strict mode
3. Field constraints
4. Optional fields
5. Nested models
6. Custom field validators
7. Model validators
8. Serialization and deserialization
9. Handling extra fields (ignore, forbid, allow)
"""