"""
Objective: Simulate three tasks competing to finish first. We'll identify the winner without waiting for all tasks to complete.

We'll practise:
- asyncio.wait()
- asyncio.FIRST_COMPLETED
- done and pending
- Task completion order
"""


import asyncio
import time


async def worker(name, duration):

    print(f"{name} started")

    await asyncio.sleep(duration)

    print(f"{name} completed")

    return f"{name} result"


async def main():

    start = time.perf_counter()

    # Create three independent tasks
    task_a = asyncio.create_task(worker("Task A", 3))
    task_b = asyncio.create_task(worker("Task B", 1))
    task_c = asyncio.create_task(worker("Task C", 2))

    # Wait until at least one task completes
    done, pending = await asyncio.wait(
        [task_a, task_b, task_c],
        return_when=asyncio.FIRST_COMPLETED
    )

    print("\nFirst completed task:")

    for task in done:
        print(task.result())

    print("\nPending tasks:")

    for task in pending:
        print(task.get_name())

    print(f"\nElapsed time: {time.perf_counter() - start:.2f} seconds")

    # Wait for remaining tasks
    await asyncio.gather(*pending)


asyncio.run(main())
