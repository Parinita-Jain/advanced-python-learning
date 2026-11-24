""""
import asyncio

async def fetch_api(api_name,duration,should_fail=False):
    print(f"{api_name}: Started")
    await asyncio.sleep(duration)
    if should_fail:
        raise ValueError(f"{api_name} failed")
    print(f"{api_name} completed")

async def main():
    result =  await asyncio.gather(
        fetch_api("User API",2),
        fetch_api("Payment API",1,should_fail=True),
        fetch_api("Product API",3), 
        return_exceptions=True
    )
    print("\nProcessing results:")
    for res in result:
        if isinstance(res, Exception):
            print("Error:",res)
        else:
            print("Success:",res)           

asyncio.run(main())

"""
#---------------
"""
import asyncio
import time

async def worker(name,duration):
    print(f"{name} strated")
    await asyncio.sleep(duration)
    print(f"{name} completed")
    return f"{name} result"
async def main():
    start=time.perf_counter()
    task_a=asyncio.create_task(worker("Task A",3))
    task_b=asyncio.create_task(worker("Task B",1))
    task_c=asyncio.create_task(worker("Task C",2))

    done,pending= await asyncio.wait(
        [task_a,task_b,task_c], 
        return_when=asyncio.FIRST_COMPLETED)
    print("First task Completed")
    for task in done:
        print(task.result())
    print("\nPending tasks:")
    for task in pending:
        print(task.get_name())      

    print(f"\nElapsed time: {time.perf_counter()-start:.2f} seconds")
    # waiting for other tasks to finish
    await asyncio.gather(*pending)

asyncio.run(main())
"""
"""
You've revised:
- asyncio.wait() - given in list or tuple of tasks
- FIRST_COMPLETED
- ALL_COMPLETED
- done and pending
- task.result()
- task.get_name()

# Without timeout: pending is always set()
done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

# With timeout: if tasks take longer than 2s, unfinished ones go into pending!
done, pending = await asyncio.wait(tasks, timeout=2.0, return_when=asyncio.ALL_COMPLETED)

"""
#--------------------
"""
import asyncio
async def fetch_api(api_name,duration):
    print(f"{api_name} : Started")
    try:
        await asyncio.sleep(duration)
        print(f"{api_name} : Completed")
        return f"{api_name} response"
    except asyncio.CancelledError:
        print(f"{api_name} : Cancelled")
        raise
async def main():
    taskA=asyncio.create_task(fetch_api("Api A",5))
    try:
        result=asyncio.wait_for(taskA,timeout=2)
    except asyncio.TimeoutError:
        print("ApiA timedout")
    taskB=asyncio.create_task(fetch_api("Api B",4))
    try:
        result=await asyncio.wait_for(asyncio.shield(taskB),timeout=2)
    except asyncio.TimeoutError:
        print("ApiB timedout but task continues")
    result=await taskB  
    print("Final result:",result)

asyncio.run(main())

"""
#--------------------
"""
import asyncio
async def producer(queue):
    for job in range(1,6):
        print(f"Producing job : {job}")
        await queue.put(job)
        await asyncio.sleep(0.5)
    await queue.put(None)
    await queue.put(None)

async def worker(name,queue):
    while True:
        job = await queue.get()
        if job is None:
            print(f"{name} stopping")
            queue.task_done()
            break
        print(f"{name} Processing JOb : {job}")
        await asyncio.sleep(1)
        print(f"{name} Completed Job : {job} ")
        queue.task_done()
async def main():
    queue = asyncio.Queue()
    worker1 = asyncio.create_task(worker("Worker 1",queue))
    worker2 = asyncio.create_task(worker("Worker 2",queue))
    await producer(queue)
    await queue.join()
    await asyncio.gather(worker1,worker2)
    print("All jobs completed!")

"""
#--------------------
'''
import asyncio
async def producer(queue):
    for job in range(1,6):
        print(f"Producing Job : {job}")
        await queue.put(job)
        await asyncio.sleep(0.5)
    await queue.pu(None)
    await queue.put(None)
#consumer
async def worker(name,queue):
    while True:
        job = await asyncio.get(queue)
        if job is None:
            print(f"{name} stopping")
            queue.task_done() #• If you forget task_done(): The counter never reaches 0, and await queue.join() will hang forever.
            break
        print(f"{name} Processing Job : {job}")
        await asyncio.sleep(0.5)
        print(f"{name} Completed Job : {job}")
        queue.task_done()   
        """
        queue.task_done() must be inside the while loop because it tracks individual items, 
        not the worker itself—every single await queue.get() inside the loop requires its own matching queue.task_done().
        """
async def main():
    queue = asyncio.Queue()
    worker1=asyncio.create_task(worker("Worker 1",queue))
    worker2=asyncio.create_task(worker("Worker 2",queue))
    await producer(queue)
    await queue.join() #• This will block until all items in the queue have been processed and marked as done.
    await asyncio.gather(worker1,worker2)   
    print("All jobs completed!")
asyncio.run(main())

'''
#---------------------
"""
import asyncio
class DatabaseConnection:
    async def __aenter__(self):
        print("Connecting to database : ")
        await asyncio.sleep(1)
        print("Database connected")
        return self
    async def __aexit__(self,exe_type,exec_value,traceback):
        print("Closing dababase connection : ")
        await asyncio.sleep(1)
        print("Database connection Closed")
    async def fetch_data(self):
        print("Fetching data : ")
        await asyncio.sleep(2)
        print("Data fetched successfully")
        return ["employee 1 ","employee 2"]
async def main():
    async with DatabaseConnection as db:
        data=await db.fetch_data()
        print("Result :",data)
asyncio.run(main()) 

"""
#-----------
from pydantic import BaseModel

class Employee(BaseModel):
    id:int
    name:str
emp_data={"id":1,"name":"Apple"}
emp1=Employee(**emp_data)
print(emp1)

"""
Step 5: Understand what happened
- BaseModel is the foundation of Pydantic models.
- We defined the expected fields and their types.
- Employee(**employee_data) passes the dictionary values as keyword arguments.
- Pydantic validates the incoming values and converts compatible types where possible.
- salary was supplied as an integer but parsed as a float.
Important distinction:

A Python dataclass primarily provides convenient data structures. Pydantic models additionally provide runtime data validation and parsing.

"""
"""
from pydantic import BaseModel, ConfigDict

class Employee(BaseModel):
    model_config = ConfigDict(strict=True)

    age: int
emp1 = Employee(age=30)
print(emp1)

emp2 = Employee(age="30")
print(emp2)

"""
#--------------------------

from pydantic import BaseModel, Field, ValidationError


class Employee(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=60)
    salary: float = Field(gt=0)


try:
    employee = Employee(
        name="Rahul",
        age=30,
        salary=55000
    )

    print(employee)

except ValidationError as e:
    print(e)

"""
Step 2: Understand the constraints
Constraint	Meaning
min_length=2	Minimum 2 characters
max_length=50	Maximum 50 characters
ge=18	Greater than or equal to 18
le=60	Less than or equal to 60
gt=0	Strictly greater than zero
"""
"""
from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    age: int
    department: str | None = None

emp = Employee(name="Rahul", age=30)

print(emp.department)

"""
#---------------------
"""
from pydantic import BaseModel,Field
from fastapi import FastAPI
class EmployeeCreate(BaseModel):
    name:str=Field(min_length=4,max_length=50)
    age:int=Field(ge=18,le=60)
    department:str
app=FastAPI(title ="Employee Management System")
employees=[]
@app.get("/")
def home():
    return {"message":"Welcome to Employee Management System"}

@app.post("/employees")
def create_employee(employee:EmployeeCreate):
    new_employee=employee.model_dump()
    new_employee["id"]=len(employees)+1
    employees.append(new_employee)
    return new_employee

@app.get("/employees")
def get_employees():
    return employees
"""
#------------
from fastapi import FastAPI,HTTPException
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
Step 3 — Test in Swagger
- Request /employees/2 — should return HTTP 200.
- Request /employees/100 — should return HTTP 404.
Understand the difference
Status code	Meaning
200	Request successful
404	Requested resource not found
422	Input validation failed
500	Internal server error
"""