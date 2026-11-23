"""
Objective: Learn how to specify expected data types for variables, function parameters and return values.
"""

#Notice that Python still executes the function despite the mismatch between the type hint and the actual argument.
def calculate_salary(
    monthly_salary: float,
    bonus: float
) -> float:

    annual_salary = (monthly_salary * 12) + bonus

    return annual_salary


def get_employee_details(
    employee_id: int,
    employee_name: str,
    skills: list[str] 
) -> dict:  # instead of dict if str is return then also executes and not give any error but it is not a good practice to do so.

    return {
        "id": employee_id,
        "name": employee_name,
        "skills": skills
    }


salary = calculate_salary(50000, 100000)

employee = get_employee_details(
    101,
    "Rahul",
    ["Python", "SQL", "Machine Learning"]
)

print("Annual salary:", salary)
print("Employee:", employee)

"""
Next concept: Optional and Union
These are useful when developing APIs and handling data that may have different types or missing values.

def get_employee(employee_id: int) -> str | None:
    if employee_id == 101:
        return "Rahul"

    return None
"""
"""
One more important concept: Any
Consider:

from typing import Any

def process_data(value: Any) -> Any:
    return value

Any essentially tells the type checker that the value can be of any type. It provides much less type safety than
specific annotations.
Annotation	Meaning
int	Integer
str	String
int \| str	Integer or string
str \| None	String or None
list[int]	List of integers
dict[str, int]	Dictionary with string keys and integer values
Any	Any type

"""
"""
What is the difference between these two annotations?
def function_a(value: Any):
    pass

def function_b(value: object):
    pass
    
Any disables most static type checking for that value, 
whereas object represents a general Python object and still requires type checking before using type-specific operations.
"""

"""
Any vs object

from typing import Any

def process_any(value: Any):
    return value.upper()

def process_object(value: object):
    return value.upper()

process_any() is generally accepted by static type checkers because Any disables most type checking for that value.



process_object() produces a type-checking error because an arbitrary object is not guaranteed to have an .upper() method.

At runtime, both functions can still execute if you pass a string. Type annotations themselves don't enforce the restriction.

def process_object(value: object):
    if isinstance(value, str):
        return value.upper()

    return None
"""
"""
Next concept: Generics and TypeVar
Generics allow you to write reusable functions and classes that preserve type information.

For example:
"""
from typing import TypeVar

T = TypeVar("T")

def get_first(items: list[T]) -> T:
    return items[0]


print(get_first([10, 20, 30]))
print(get_first(["Python", "SQL", "ML"]))

"""
Here, T represents a type that is determined from the input.
- Integer list → returns an integer.
- String list → returns a string.
This is useful when building reusable utilities, data-processing functions and libraries.
"""

"""
One important distinction
- TypeVar allows a function to preserve relationships between input and output types.
- Any effectively opts out of most static type checking.
- object represents a general object and requires type narrowing before type-specific operations.
"""

"""
Let's consolidate what you've learned.
Concept	Purpose
int, str, float	Basic type annotations
list[int], dict[str, int]	Collection annotations
int \| str	Union types
str \| None	Optional return values
Any	Flexible typing
object	General object type
TypeVar	Reusable generic functions
"""