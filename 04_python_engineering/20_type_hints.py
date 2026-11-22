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