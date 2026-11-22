
import asyncio
import time


async def task(name, duration):

    print(f"{name} started")

    await asyncio.sleep(duration)

    print(f"{name} completed")

    return f"{name} result"


async def main():

    start = time.perf_counter()

    result1 = await task("Task A", 3)
    result2 = await task("Task B", 2)
    result3 = await task("Task C", 1)

    print("\nResults:")
    print(result1)
    print(result2)
    print(result3)

    end = time.perf_counter()

    print(f"\nTotal time: {end - start:.2f} seconds")


asyncio.run(main())

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(
    task("Task A", 3),
    task("Task B", 2),
    task("Task C", 1)
    
    )
    end = time.perf_counter()
    for result in results:
        print(result)

    print(f"\nTotal time: {end - start:.2f} seconds")

asyncio.run(main())

async def main():
    start = time.perf_counter()

    task_a = asyncio.create_task(task("A", 3))
    task_b = asyncio.create_task(task("B", 2))
    task_c = asyncio.create_task(task("C", 1))

    result_a = await task_a
    result_b = await task_b
    result_c = await task_c

    print("\nResults:")
    print(result_a)     
    print(result_b)
    print(result_c)

    end = time.perf_counter()

    print(f"\nTotal time: {end - start:.2f} seconds")

asyncio.run(main())

async def main():
    start = time.perf_counter()

    tasks = [
        asyncio.create_task(task("A", 3)),
        asyncio.create_task(task("B", 2)),
        asyncio.create_task(task("C", 1))
    ]

    results = await asyncio.gather(*tasks)

    print("\nResults:")
    for result in results:
        print(result)

    end = time.perf_counter()

    print(f"\nTotal time: {end - start:.2f} seconds")


asyncio.run(main())

