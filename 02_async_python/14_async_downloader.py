"""
Objective: Simulate downloading three files concurrently and compare asynchronous execution with a blocking function.

We'll practise:
- asyncio.gather()
- asyncio.sleep()
- asyncio.to_thread()
- Blocking vs non-blocking operations
"""

import asyncio
import time


# Simulated asynchronous download
async def async_download(filename, duration):

    print(f"Starting async download: {filename}")

    await asyncio.sleep(duration)

    print(f"Completed async download: {filename}")

    return f"{filename} downloaded"


# Simulated synchronous, blocking download
def sync_download(filename, duration):

    print(f"Starting sync download: {filename}")

    time.sleep(duration)

    print(f"Completed sync download: {filename}")

    return f"{filename} downloaded"


async def main():

    # Example 1: Concurrent asynchronous downloads
    print("\n--- Async downloads ---")

    start = time.perf_counter()

    results = await asyncio.gather(
        async_download("file_A", 3),
        async_download("file_B", 2),
        async_download("file_C", 1)
    )

    print("Results:", results)

    print(f"Async time: {time.perf_counter() - start:.2f} seconds")


    # Example 2: Run blocking functions in threads
    print("\n--- Blocking downloads using to_thread ---")

    start = time.perf_counter()

    results = await asyncio.gather(
        asyncio.to_thread(sync_download, "file_A", 3),
        asyncio.to_thread(sync_download, "file_B", 2),
        asyncio.to_thread(sync_download, "file_C", 1)
    )

    print("Results:", results)

    print(f"Threaded time: {time.perf_counter() - start:.2f} seconds")


asyncio.run(main())
"""
(advanced-python-learning) PS C:\Users\sagar\Documents\advanced-python-learning> python .\02_async_python\14_async_downloader.py

--- Async downloads ---
Starting async download: file_A
Starting async download: file_B
Starting async download: file_C
Completed async download: file_C
Completed async download: file_B
Completed async download: file_A
Results: ['file_A downloaded', 'file_B downloaded', 'file_C downloaded']
Async time: 3.02 seconds

--- Blocking downloads using to_thread ---
Starting sync download: file_A
Starting sync download: file_B
Starting sync download: file_C
Completed sync download: file_C
Completed sync download: file_B
Completed sync download: file_A
Results: ['file_A downloaded', 'file_B downloaded', 'file_C downloaded']
Threaded time: 3.01 seconds
(advanced-python-learning) PS C:\Users\sagar\Documents\advanced-python-learning>                                                
"""
"""
The output and execution time (~3.00 seconds) will be completely identical—both versions run concurrently in the background threads.
Under the hood, asyncio.gather() automatically wraps every coroutine you pass to it (including the coroutine returned by asyncio.to_thread()) inside asyncio.create_task() anyway.

Side-by-Side Comparison

python
# Your current way (shorthand)
results = await asyncio.gather(
    asyncio.to_thread(sync_download, "file_A", 3),
    asyncio.to_thread(sync_download, "file_B", 2),
    asyncio.to_thread(sync_download, "file_C", 1)
)

# Wrapping in create_task first (explicit)
t1 = asyncio.create_task(asyncio.to_thread(sync_download, "file_A", 3))
t2 = asyncio.create_task(asyncio.to_thread(sync_download, "file_B", 2))
t3 = asyncio.create_task(asyncio.to_thread(sync_download, "file_C", 1))
results = await asyncio.gather(t1, t2, t3)
Use code with caution.

When Does Wrapping in create_task() First Actually Matter?

Even though gather() gives the exact same result here, creating the tasks beforehand gives you three practical advantages:
1. You get handles to cancel or inspect individual tasks:
	• If t1, t2, and t3 are stored in variables, you can call t1.cancel(), t1.done(), or t1.set_name("DownloadA") while they are running. When you pass to_thread(...) directly into gather(), you don't hold references to the individual tasks.
2. Tasks start running before you reach gather():
	• With create_task(), the threads are scheduled immediately. If you need to run some other await setup steps before calling await asyncio.gather(t1, t2, t3), the downloads are already progressing in the background while that setup runs.
3. You can pass them to asyncio.wait() or asyncio.as_completed():
	• As you saw earlier, asyncio.wait() strictly requires Task objects rather than raw coroutines.

One Caveat Specific to to_thread()

Unlike pure async tasks, a running thread cannot be forcefully interrupted mid-way if you call t1.cancel().
• If t1 hasn't started yet, t1.cancel() prevents it from running.
• If sync_download is already inside time.sleep(3) on a worker thread, calling t1.cancel() marks the Task as cancelled in asyncio, but the background thread will still finish sleeping for 3 seconds before freeing up.
Would you like to see:
• How to safely stop a blocking thread using threading.Event when cancelling to_thread()
• Why to_thread() is great for I/O (files, APIs) but bad for CPU-heavy math (due to the Python GIL)

"""