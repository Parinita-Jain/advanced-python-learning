"""
Stage 6 – Project 23: Employee Management API using FastAPI
New project
 Beginner to intermediate


What we'll build

A REST API that allows us to:
1. Add employees.
2. Retrieve all employees.
3. Retrieve an employee by ID.
4. Update employee details.
5. Delete an employee.
6. Validate incoming data using Pydantic.
We'll build this incrementally, understanding each concept as we go.
Step 1: Create a separate file
Inside your existing folder:


1. REST API (The "What")

REST (Representational State Transfer) is a set of standard rules and conventions for how systems communicate over the internet using HTTP. It dictates what your endpoints should look like and how they should behave:
• Resources: Treating data like employees as resources accessible via URLs (e.g., /employees or /employees/101).
• HTTP Methods: Mapping standard actions to specific HTTP verbs—POST to add, GET to retrieve, PUT/PATCH to update, and DELETE to remove.
• Data Format: Exchanging data using standard formats like JSON.

2. FastAPI (The "How")

FastAPI is the actual Python library you install and write code with to implement those REST rules. Without a framework like FastAPI, you would have to manually parse raw HTTP requests, validate JSON data from scratch, and write routing logic yourself. FastAPI does this heavy lifting for you.

How They Work Together in Your Project


REST API Concept (The Rule)	FastAPI Implementation (The Code)
Retrieve all employees via GET	@app.get("/employees")
Add a new employee via POST	@app.post("/employees")
Validate incoming JSON payload	def create_employee(emp: EmployeeSchema): (using Pydantic)

Uvicorn is the web server that actually runs your FastAPI application and connects it to the network.
FastAPI is just a Python framework—it knows how to route URLs, validate data, and run your business logic, but it does not know how to listen to network ports or speak raw HTTP over the internet on its own. Uvicorn acts as the bridge between the outside world and your Python code.

How They Divide the Work

• Uvicorn (The Receptionist / Server): It listens on a network port (like localhost:8000), accepts incoming raw HTTP connections from browsers or mobile apps, translates those network bytes into a format Python understands, and hands them off to FastAPI.
• FastAPI (The Worker / Application): It receives that translated request from Uvicorn, matches the URL (e.g., /employees), validates the data using Pydantic, runs your function, and hands the result back to Uvicorn to send over the network.

Why Uvicorn Specifically?

Python web frameworks communicate with web servers using a standard interface. Older frameworks like Flask used WSGI (synchronous, handling one request at a time per worker). FastAPI is built on a modern standard called ASGI (Asynchronous Server Gateway Interface), which supports asynchronous code (async/await) to handle many concurrent connections efficiently.
Uvicorn is a lightning-fast ASGI server built specifically to run modern asynchronous Python frameworks like FastAPI.

Summary Analogy

If your Employee Management API is a restaurant:
• REST API is the menu structure and ordering etiquette.
• FastAPI is the kitchen staff preparing the food (processing the data).
• Uvicorn is the front-of-house host opening the doors, taking orders from customers,
 and delivering the finished plates back to the tables.

Step 2: Install FastAPI and Uvicorn
Open the terminal at your project root:
uv add fastapi "uvicorn[standard]"


What are these?
- FastAPI: Framework used to build APIs using Python.
- Uvicorn: ASGI server that runs your FastAPI application.
Step 3: Write your first FastAPI application
Add this code to 23_fastapi_employee_api.py.
"""
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Create FastAPI application
app = FastAPI(title="Employee Management API")


# Pydantic request model
class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=60)
    department: str


# Temporary in-memory employee storage
employees = []


# First API endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Employee Management API"}


# Add employee
@app.post("/employees")
def create_employee(employee: EmployeeCreate):
    new_employee = employee.model_dump()

    new_employee["id"] = len(employees) + 1

    employees.append(new_employee)

    return new_employee
"""
"""
# Retrieve all employees
@app.get("/employees")
def get_employees():
    return employees
"""
"""
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return {"message": "Employee not found"}

"""
"""
@app.get("/employees")
def get_employees(department: str | None = None):
    if department:
        return [
            employee for employee in employees
            if employee["department"].lower() == department.lower()
        ]

    return employees
"""
"""
Step 4: Understand the code
1. Creating the application
app = FastAPI(title="Employee Management API")



This creates the FastAPI application instance.

2. Pydantic request model
class EmployeeCreate(BaseModel):    name: str    age: int    department: str



This defines the expected structure of employee data.

FastAPI automatically uses Pydantic to validate incoming request data.

3. Creating an endpoint
@app.get("/")



This decorator tells FastAPI that the function below handles HTTP GET requests to the root URL.

Similarly:
@app.post("/employees")



Handles HTTP POST requests to /employees.

4. Extracting validated data
new_employee = employee.model_dump()



Remember our Pydantic lessons? This converts the validated Pydantic object into a Python dictionary.
Step 5: Run the application
From your project root, execute:
uv run uvicorn 04_python_engineering.23_fastapi_employee_api:app --reload


You should see something similar to:
Uvicorn running on http://127.0.0.1:8000
or in browser - http://localhost:8000/docs
Application startup complete.


Keep this terminal running.
Step 6: Open the interactive API documentation
Open your browser and visit:
FastAPI Swagger documentation







realpython.com


You should see your API endpoints:
- GET /
- POST /employees
- GET /employees
You can execute API requests directly from this page without writing a separate frontend.

Your first experiment
In Swagger, expand POST /employees, click Try it out, and submit:
{
  "name": "Rahul",
  "age": 30,
  "department": "Data Science"
}


Expected response:
{
  "name": "Rahul",
  "age": 30,
  "department": "Data Science",
  "id": 1
}


Then try submitting:
{
  "name": "Rahul",
  "age": 15,
  "department": "Data Science"
}


You should receive HTTP 422 Unprocessable Entity because our Pydantic model requires age to be at least 18.

Important: Employee records are currently stored in memory. They will disappear when you restart the application. We'll explore persistent storage later.
Knowledge check
When a client sends an invalid age of 15 to our POST endpoint, which component is responsible for validating the age and rejecting the request?

A. Uvicorn

B. Pydantic

C. Git

D. Python's print() function

First get the application running and test both requests. Then answer the question.

1. GET (Read / Retrieve)
2. POST (Create / Add)


HTTP Method	Action	Project 23 Endpoint	Sends JSON Body?
POST	Create (Add employee)	POST /employees	Yes (new employee data)
GET	Read (Get all or one employee)	GET /employees or GET /employees/{id}	No
PUT / PATCH	Update (Edit employee details)	PUT /employees/{id}	Yes (updated fields)
DELETE	Delete (Remove employee)	DELETE /employees/{id}	No

"""
"""
Step 2: Understand the URL parameter
@app.get("/employees/{employee_id}")



The {employee_id} is a path parameter.

For example:
GET /employees/1
GET /employees/2
GET /employees/5


FastAPI extracts the ID from the URL and passes it to the function.
def get_employee(employee_id: int):



The int annotation tells FastAPI to expect an integer.
Step 3: Test in Swagger
Open:
FastAPI Swagger documentationExpand GET /employees/{employee_id}.

Try employee ID 5, which appeared in your earlier successful POST response.

You should get Ariel's employee record.

employees = [
    {"id": 1, "name": "Rohan", "role": "Developer"},  # <-- dictionary
    {"id": 2, "name": "Sneha", "role": "Designer"}    # <-- dictionary
]

 employees is a Python list containing dictionaries (not Pydantic models).

How You Can Tell

Look at this specific line in your loop:
python
if employee["id"] == employee_id:
Use code with caution.
• Square brackets ["id"] only work on Python dictionaries.
• If employee were a Pydantic model object, using square brackets would crash your app with a 
TypeError: 'Employee' object is not subscriptable. With a Pydantic model, you would have to use dot notation instead (employee.id).

from fastapi import HTTPException

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
            
    raise HTTPException(status_code=404, detail="Employee not found")

"""

"""
Path parameter vs Query parameter
1. Path parameter
/employees/5


Defined as:
@app.get("/employees/{employee_id}")def get_employee(employee_id: int):



The employee ID is part of the URL path.

2. Query parameter
/employees?id=5


Defined as:
@app.get("/employees")def get_employee(id: int):



Here, id is passed after the ? symbol as a query parameter.
Feature	Path parameter	Query parameter
Location	Within URL path	After ?
Example	/employees/5	/employees?id=5
Typical use	Identify a specific resource	Filter, search or customise results

Remember: {employee_id} inside the route declaration indicates a path parameter.
"""

"""
/employees?department=IT uses a query parameter.
- ? marks the beginning of the query string.
- department is the parameter name.
- IT is its value.
Let's add this to your API
In 23_fastapi_employee_api.py, add:
@app.get("/employees")def get_employees(department: str | None = None):    if department:        return [            employee for employee in employees            if employee["department"].lower() == department.lower()        ]    return employees



Important: Replace your existing get_employees() function with this version. Don't create a second GET /employees route.
Test in Swagger
Try these URLs:
URL	Expected behaviour
/employees	Returns all employees
/employees?department=IT	Returns only IT employees
/employees?department=HR	Returns only HR employees

FastAPI automatically identifies department as a query parameter because it is not part of the route path.
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
app=FastAPI(title="Employee Management System")
class EmployeeCreate(BaseModel):
    name:str=Field(min_length=1,max_length=20)
    id:int=Field(le=100)
    department:str
emps=[]
@app.get("/")
def home():
    return {"message":"Hello Employees"}
@app.post("/EmployeeInput")
def employeeInput(employee:EmployeeCreate):
    new_employee=employee.model_dump()
    new_employee["id"]=len(emps)+1
    emps.append(new_employee)
    return f"{new_employee} Added"
@app.get("/All_employees")
def all_employees():
    return emps

@app.get("/ParticularEmployee/{id}")
def particular_id(id:int):
    for e in emps:
        if e["id"]==id:
            return e
    return {"message":"employee not found"}

@app.get("/ParticularDepartment")
def dept(d:str|None=None):
    if d:
        return [i for i in emps if i["department"].lower()==d.lower()]
    return emps

@app.get("/employeesHTTPException/{employee_id}")
def get_employee(employee_id: int):
    for employee in emps:
        if employee["id"] == employee_id:
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

"""
We use raise HTTPException(...) because returning a dictionary sends an HTTP 200 OK status code, telling the client the request succeeded when it actually failed.
In FastAPI (and web APIs in general), the HTTP status code is how the server communicates what happened to the frontend, mobile app, or other services.

"""
"""
Next: Project 23 — Add an UPDATE endpoint (PUT)
We'll now implement the next CRUD operation:
Operation	HTTP method	Purpose
Create	POST	Add an employee
Read	GET	Retrieve employees
Update	PUT	Update an employee
Delete	DELETE	Remove an employee

Next step: We'll create a PUT endpoint that updates an employee's name, age and department 
using their employee ID. We'll also introduce the difference between PUT and PATCH.

"""
"""
Step 1: Create the PUT endpoint
Our objective is to update an existing employee's details using their employee ID.

For example, suppose employee ID 2 currently has:
{
    "id": 2,
    "name": "Apple",
    "age": 21,
    "department": "IT"
}


We want to change the details to:
{
    "name": "Apple",
    "age": 25,
    "department": "Finance"
}


1. Add a new Pydantic model
Place this below your existing EmployeeCreate class:
class EmployeeUpdate(BaseModel):    
    name: str = Field(min_length=2, max_length=50)    
    age: int = Field(ge=18, le=60)    
    department: str



Why create another model?
- EmployeeCreate defines the structure for creating an employee.
- EmployeeUpdate defines the structure for updating an employee.
For now, both have the same fields. Later, we'll explore partial updates using PATCH.
2. Add the PUT endpoint
Add this below your existing GET endpoints:
Project 23 — Step 4: Create a PATCH endpoint
Suppose employee ID 2 has these details:
{
  "id": 2,
  "name": "Apple",
  "age": 25,
  "department": "Finance"
}


Now you want to change only the age from 25 to 26.

With PUT, you send all three fields. With PATCH, you send only the field you want to change.
1. Create a new Pydantic model
Add this below your EmployeeUpdate class:

Why None defaults?

Because the client is allowed to omit fields it doesn't want to update.

================
3. Understand two important concepts
A. exclude_unset=True

Suppose the client sends:
{
    "age": 26
}


Pydantic knows that only age was supplied.

Therefore:
updated_data.model_dump(exclude_unset=True)



produces:
{"age": 26}



It does not include name or department.

B. employee.update(update_fields)

This is a Python dictionary method.

It updates only the supplied keys while preserving the other existing keys.
4. Test in Swagger
Open PATCH /UpdateByPatchEmployees/{employee_id}.

Employee ID: 2

Request body:
{
    "age": 26
}


Expected response:
{
    "name": "Apple",
    "age": 26,
    "department": "Finance",
    "id": 2
}


Notice that the name and department remain unchanged.

Knowledge check
Why do we use exclude_unset=True instead of simply calling model_dump()?

A. To remove all fields containing strings.

B. To include only the fields explicitly supplied by the client.

C. To convert all values into strings.

D. To prevent Pydantic from validating the request.

Try implementing and testing PATCH first.

Next: Project 23 — Step 5: DELETE endpoint
Now we'll implement the final CRUD operation: deleting an employee.

Add this endpoint:

"""

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
app=FastAPI(title="Employee Management System")
class EmployeeCreate(BaseModel):
    name:str=Field(min_length=1,max_length=20)
    age:int=Field(le=100)
    department:str

class EmployeeUpdate(BaseModel):    
    name: str = Field(min_length=2, max_length=50)    
    age: int = Field(ge=18, le=60)    
    department: str

class EmployeePatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge=18, le=60)
    department: str | None = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str

emps=[]
@app.get("/")
def home():
    return {"message":"Hello Employees"}
@app.post("/EmployeeInput")
def employeeInput(employee:EmployeeCreate):
    new_employee=employee.model_dump()
    new_employee["id"]=len(emps)+1
    emps.append(new_employee)
    return f"{new_employee} Added"
@app.get("/All_employees")
def all_employees():
    return emps

@app.get("/ParticularEmployee/{id}")
def particular_id(id:int):
    for e in emps:
        if e["id"]==id:
            return e
    return {"message":"employee not found"}

@app.get("/ParticularDepartment")
def dept(d:str|None=None):
    if d:
        return [i for i in emps if i["department"].lower()==d.lower()]
    return emps
@app.get("/employeesHTTPException/{employee_id}")
def get_employee(employee_id: int):
    for employee in emps:
        if employee["id"] == employee_id:
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

@app.put("/UpdateByPutEmployees/{employee_id}")
def update_employee(employee_id: int, updated_employee: EmployeeUpdate):

    for employee in emps:
        if employee["id"] == employee_id:

            employee["name"] = updated_employee.name
            employee["age"] = updated_employee.age
            employee["department"] = updated_employee.department

            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

@app.patch("/UpdateByPatchEmployees/{employee_id}")
def patch_employee(employee_id: int, updated_data: EmployeePatch):

    for employee in emps:
        if employee["id"] == employee_id:

            update_fields = updated_data.model_dump(exclude_unset=True)

            employee.update(update_fields)

            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

@app.delete("/DeleteEmployee/{employee_id}")
def delete_employee(employee_id: int):

    for index, employee in enumerate(emps):
        if employee["id"] == employee_id:
            deleted_employee = emps.pop(index)
            return {
                "message": "Employee deleted successfully",
                "employee": deleted_employee
            }

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )
@app.get("/All_employeesResponse_model", response_model=list[EmployeeResponse])
def all_employeesResponse_model():
    return emps
#--------
"""
What's next?
Before we move to the next project, we'll improve this API with three important FastAPI concepts:
1. Response models — control and validate what the API returns.
2. HTTP status codes — return appropriate codes such as 201 Created and 204 No Content.
3. Separating request and response models — structure APIs professionally.
Let's start with Response Models in the next lesson.
"""
"""
Even though age exists in your original employee dictionary, FastAPI excludes it from the response 
because it isn't defined in EmployeeResponse.
4. What does response_model do?
It provides three important benefits:
- Validates the outgoing response.
- Filters out fields not included in the response model.
- Documents the expected response structure in Swagger.
"""