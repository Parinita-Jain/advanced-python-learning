"""
Objective: Learn how to execute multiple blocking I/O operations concurrently using Python threads.

We'll simulate downloading three files from different servers.
"""


import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


# Locate the sample_files folder relative to this script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FILE_FOLDER = PROJECT_ROOT / "sample_files"


def read_file(file_path):

    print(f"Reading: {file_path.name}")

    # Simulate a small I/O delay
    time.sleep(2)

    content = file_path.read_text(encoding="utf-8")

    print(f"Finished reading: {file_path.name}")

    return content


def main():

    start_time = time.perf_counter()

    files = [
        FILE_FOLDER / "file1.txt",
        FILE_FOLDER / "file2.txt",
        FILE_FOLDER / "file3.txt"
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = [
            executor.submit(read_file, file)
            for file in files
        ]

        results = [future.result() for future in futures]

    print("\n----- FILE CONTENTS -----")

    for index, content in enumerate(results, start=1):
        print(f"\nFile {index}:")
        print(content)

    end_time = time.perf_counter()

    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()

"""
We use threads here instead of async/await because Python’s standard file operations (file_path.read_text()) are strictly synchronous and blocking—the operating system does not provide true cross-platform asynchronous disk file I/O for standard Python.
And yes, you can await a ThreadPoolExecutor inside an async function using asyncio.to_thread() or loop.run_in_executor().

1. Why Not Pure async/await for File Reading?

• Network I/O vs. Disk File I/O: Operating systems have native non-blocking APIs for network sockets (used by aiohttp or asyncio streams), so a single thread can manage thousands of network calls without blocking. However, standard disk file reading (open(), .read_text()) blocks the thread until the OS fetches the bytes from the drive.
• What happens if you put read_text() inside async def: Even if you put file_path.read_text() inside an async def function, there is no await inside .read_text(), so it freezes the entire event loop until the file finishes reading.
• Even aiofiles uses threads: Popular libraries like aiofiles (which give you async with aiofiles.open(...)) actually just wrap standard blocking file calls inside a background ThreadPoolExecutor behind the scenes!

2. How to await a ThreadPoolExecutor Inside async/await

When your application is already using asyncio (for example, a FastAPI server or an async web scraper) and you need to read files without freezing the event loop, you offload the blocking function to a thread pool and await it.
You have two ways to do this in Python:

Option A: asyncio.to_thread() (Modern & Simplest — Python 3.9+)

This automatically uses a default ThreadPoolExecutor and turns your blocking read_file function into an awaitable coroutine:
python
import asyncio
import time
from pathlib import Path

def read_file(file_path):  # Regular blocking function!
    print(f"Reading: {file_path.name}")
    time.sleep(2)
    return file_path.read_text(encoding="utf-8")

async def main():
    files = [Path("file1.txt"), Path("file2.txt"), Path("file3.txt")]

    # Runs each blocking read_file() on a worker thread and awaits all of them
    results = await asyncio.gather(
        *(asyncio.to_thread(read_file, f) for f in files)
    )
    print(results)

asyncio.run(main())
Use code with caution.

Option B: loop.run_in_executor() with a Custom ThreadPoolExecutor

If you want strict control over max_workers (e.g., limiting disk reads to 3 threads), pass your own ThreadPoolExecutor into loop.run_in_executor():
python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def main():
    loop = asyncio.get_running_loop()
    files = [Path("file1.txt"), Path("file2.txt"), Path("file3.txt")]

    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [
            loop.run_in_executor(executor, read_file, f)
            for f in files
        ]
        results = await asyncio.gather(*tasks)
Use code with caution.

Quick Mental Model: When to Use Which


Workload Type	Best Tool	Why
Network I/O (APIs, HTTP, WebSockets, Async DB drivers)	Pure async/await (asyncio)	OS handles non-blocking sockets natively on 1 thread with tiny memory overhead.
Blocking I/O (Disk files, time.sleep, legacy libraries like requests)	ThreadPoolExecutor or asyncio.to_thread()	Offloads the blocking wait to OS threads so your main thread/event loop doesn't freeze.
Heavy CPU Math (Data crunching, image/video encoding)	ProcessPoolExecutor (multiprocessing)	Bypasses Python's GIL across multiple CPU cores.

Would you like to see:
• How aiofiles works under the hood compared to asyncio.to_thread()
• How to combine network async downloads + threaded disk writes in a single pipeline

"""