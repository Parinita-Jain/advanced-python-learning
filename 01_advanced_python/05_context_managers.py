
# Using Python's built-in context manager

file_path = "employees.txt"

with open(file_path, "w") as file:
    file.write("Rahul,50000\n")
    file.write("Priya,65000\n")

print("File writing completed!")


# Reading the file

with open(file_path, "r") as file:
    content = file.read()
    print(content)

print("File closed automatically:", file.closed)


# Creating our own context manager

class FileManager:

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print("Opening file...")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing file...")
        self.file.close()


with FileManager("custom.txt", "w") as file:
    file.write("Learning custom context managers!")

with FileManager("custom.txt", "r") as file:
    content = file.read()
    print(content)

print("Custom file operation completed.")
