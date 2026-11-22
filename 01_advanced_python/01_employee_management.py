
class Employee:

    # Constructor
    def __init__(self, name, employee_id, monthly_salary):
        self.name = name
        self.employee_id = employee_id
        self.monthly_salary = monthly_salary

    # Instance method
    def calculate_annual_salary(self):
        return self.monthly_salary * 12

    # Instance method
    def display_details(self):
        print("Employee Name:", self.name)
        print("Employee ID:", self.employee_id)
        print("Monthly Salary:", self.monthly_salary)
        print("Annual Salary:", self.calculate_annual_salary())


    def increase_salary(self, percentage):
        self.monthly_salary += self.monthly_salary * percentage / 100


# Creating objects
emp1 = Employee("Rahul", 101, 50000)
emp2 = Employee("Priya", 102, 65000)

# Calling methods
emp1.display_details()

print("--------------------")

emp2.display_details()

emp1.increase_salary(10)
emp1.display_details()
