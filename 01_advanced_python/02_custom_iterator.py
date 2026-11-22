
class EmployeeIterator:

    def __init__(self, employees):
        self.employees = employees
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.employees):
            employee = self.employees[self.index]
            self.index += 1
            return employee

        raise StopIteration


employees = ["Rahul", "Priya", "Amit", "Sneha"]

iterator = EmployeeIterator(employees)

print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))

#print(next(iterator))

for employee in iterator:
    print("Employee:", employee)

print("--------------------")
iterator = EmployeeIterator(employees)

print(next(iterator))
print(next(iterator))

for employee in iterator:
    print(employee)

print("--------------------")   
print(list(iterator))