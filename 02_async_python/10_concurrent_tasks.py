"""
Objective: Simulate calling three independent APIs concurrently and collect their responses.

We'll practise:
- asyncio.gather()
- asyncio.create_task()
- Concurrent execution
- Result ordering
- Execution timing
"""

import asyncio
import time


async def fetch_api(api_name, duration):

    print(f"{api_name}: Request started")

    await asyncio.sleep(duration)

    print(f"{api_name}: Response received")

    return {
        "api": api_name,
        "status": "success",
        "response_time": duration
    }


async def main():

    start = time.perf_counter()

    results = await asyncio.gather(
        fetch_api("User API", 3),
        fetch_api("Payment API", 2),
        fetch_api("Product API", 1)
    )

    print("\nAPI Responses:")

    for result in results:
        print(result)

    print(f"\nTotal time: {time.perf_counter() - start:.2f} seconds")

    print("\n--- Using asyncio.create_task() ---\n")
    start = time.perf_counter()
    task1 = asyncio.create_task(fetch_api("User API", 3))
    task2 = asyncio.create_task(fetch_api("Payment API", 2))
    task3 = asyncio.create_task(fetch_api("Product API", 1))

    results = await asyncio.gather(task1, task2, task3)

    print(results)

    print(f"\nTotal time: {time.perf_counter() - start:.2f} seconds")   


asyncio.run(main())
