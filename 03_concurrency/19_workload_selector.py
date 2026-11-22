"""
This is our final project in the Concurrency section.

So far, we've studied:
- asyncio for asynchronous I/O.
- ThreadPoolExecutor for concurrent I/O-bound tasks.
- ProcessPoolExecutor for CPU-bound tasks.
Now let's build a practical program that demonstrates all three approaches.
"""


import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# ----------------------------------
# 1. ASYNCIO: Simulated API requests
# ----------------------------------

async def api_request(api_name):

    print(f"Starting API request: {api_name}")

    await asyncio.sleep(2)

    print(f"Completed API request: {api_name}")

    return f"{api_name} response received"


async def run_async_apis():

    start = time.perf_counter()

    results = await asyncio.gather(
        api_request("API_A"),
        api_request("API_B"),
        api_request("API_C")
    )

    print("\nAsync API results:", results)
    print(f"Async execution time: {time.perf_counter() - start:.2f} seconds")


# ----------------------------------
# 2. THREADING: Blocking I/O tasks
# ----------------------------------

def read_file(file_path):

    print(f"Reading {file_path}")

    time.sleep(2)

    return f"{file_path} read successfully"


def run_threaded_tasks():

    start = time.perf_counter()

    files = ["file1.txt", "file2.txt", "file3.txt"]

    with ThreadPoolExecutor(max_workers=3) as executor:

        results = list(executor.map(read_file, files))

    print("\nThread results:", results)
    print(f"Thread execution time: {time.perf_counter() - start:.2f} seconds")


# ----------------------------------
# 3. MULTIPROCESSING: CPU-bound tasks
# ----------------------------------

def calculate_sum_of_squares(numbers):

    total = 0

    for number in numbers:
        total += number * number

    return total


def run_parallel_calculations():

    start = time.perf_counter()

    ranges = [
        range(1, 1_000_001),
        range(1_000_001, 2_000_001),
        range(2_000_001, 3_000_001)
    ]

    with ProcessPoolExecutor(max_workers=3) as executor:

        results = list(
            executor.map(calculate_sum_of_squares, ranges)
        )

    print("\nMultiprocessing results:", results)
    print(f"Multiprocessing execution time: {time.perf_counter() - start:.2f} seconds")


# ----------------------------------
# MAIN
# ----------------------------------

def main():

    print("\n========== ASYNCIO ==========")

    asyncio.run(run_async_apis())

    print("\n========== THREADING ==========")

    run_threaded_tasks()

    print("\n========== MULTIPROCESSING ==========")

    run_parallel_calculations()


if __name__ == "__main__":
    main()
