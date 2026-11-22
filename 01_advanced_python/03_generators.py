
def employee_generator(total_employees):

    for i in range(1, total_employees + 1):
        employee = f"Employee_{i}"
        print(f"Generating: {employee}")

        yield employee


# Create generator
employees = employee_generator(5)

print("Generator created!")

"""
# Retrieve employees one at a time
print(next(employees))
print(next(employees))
print(next(employees))
"""

for employee in employees:
    print("Received:", employee)
