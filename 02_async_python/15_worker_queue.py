"""
Objective: Create a producer that generates jobs and two workers that process those jobs concurrently.

We'll practise:
- asyncio.Queue
- queue.put() and queue.get()
- queue.task_done()
- queue.join()
- Sentinel values (None)
"""

import asyncio


# Producer: creates jobs
async def producer(queue):

    for job in range(1, 6):

        print(f"Producing job {job}")

        await queue.put(job)

        await asyncio.sleep(0.5)

    # Send termination signals to both workers
    await queue.put(None)
    await queue.put(None)


# Consumer: processes jobs
async def worker(name, queue):

    while True:

        job = await queue.get()

        if job is None:
            print(f"{name} stopping")
            queue.task_done()
            break

        print(f"{name} processing job {job}")

        await asyncio.sleep(1)

        print(f"{name} completed job {job}")

        queue.task_done()


async def main():

    queue = asyncio.Queue()

    # Create two workers
    worker1 = asyncio.create_task(worker("Worker 1", queue))
    worker2 = asyncio.create_task(worker("Worker 2", queue))

    # Start producer
    await producer(queue)

    # Wait until every queued item is marked done
    await queue.join()

    # Wait for workers to exit
    await asyncio.gather(worker1, worker2)

    print("All jobs completed!")


asyncio.run(main())

"""
Both worker1 and worker2 share the exact same single queue object, and queue.get() permanently removes an item from the queue when a worker takes it. Because one None can only be picked up by one worker, you must put two Nones into the queue so both workers get a stop signal.

1. There Is Only One Shared Queue (Not Separate Queues)

When you write:
python
worker1 = asyncio.create_task(worker("Worker 1", queue))
worker2 = asyncio.create_task(worker("Worker 2", queue))
Use code with caution.
You are not giving worker1 its own private queue and worker2 its own private queue. Both workers are pulling items from the exact same shared line (like two cashiers serving customers from a single waiting line).

2. Why None Must Be Put Twice

Every time a worker runs job = await queue.get(), that item is consumed and removed from the queue—the other worker never sees it.
Here is what happens at the end of the producer loop if you only put None once:
1. producer puts a single None into the queue: [None].
2. Worker 1 wakes up, calls await queue.get(), and takes that None. The queue is now empty ([]).
3. Worker 1 sees job is None, prints "Worker 1 stopping", and breaks out of its loop.
4. Worker 2 is still running its while True: loop, sitting on job = await queue.get(), waiting forever for an item that never arrives!
5. Your program hangs forever at await asyncio.gather(worker1, worker2) because Worker 2 never exits.
By putting None twice ([None, None]):
• Worker 1 grabs the first None and stops.
• Worker 2 grabs the second None and stops.

"""