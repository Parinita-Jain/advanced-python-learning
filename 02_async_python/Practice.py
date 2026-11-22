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