"""
Objective: Build an API request manager that handles slow responses using timeouts. We'll also learn how to protect a task from cancellation using asyncio.shield().

We'll practise:
- asyncio.wait_for()
- asyncio.shield()
- TimeoutError
- Task cancellation
"""

import asyncio


async def fetch_api(api_name, duration):

    print(f"{api_name}: Started")

    try:
        await asyncio.sleep(duration)
        print(f"{api_name}: Completed")
        return f"{api_name} response"

    except asyncio.CancelledError:
        print(f"{api_name}: Cancelled")
        raise


async def main():

    # Example 1: Request with timeout
    print("\n--- Example 1: wait_for ---")

    try:
        result = await asyncio.wait_for(
            fetch_api("API A", 5),
            timeout=2
        )

        print("Result:", result)

    except TimeoutError:
        print("API A timed out!")


    # Example 2: Protect task using shield
    print("\n--- Example 2: shield ---")

    task = asyncio.create_task(fetch_api("API B", 4))

    try:
        result = await asyncio.wait_for(
            asyncio.shield(task),
            timeout=2
        )

        print("Result:", result)

    except TimeoutError:
        print("API B timed out, but task continues!")

    # Allow the protected task to finish
    result = await task
    print("Final result:", result)


asyncio.run(main())

"""
Step 4 — Understand the difference
Example 1: asyncio.wait_for()
await asyncio.wait_for(    fetch_api("API A", 5),    timeout=2)



- API A needs 5 seconds.
- We allow only 2 seconds.
- wait_for() cancels the underlying task when the timeout expires.
- CancelledError is raised inside the coroutine.
- TimeoutError is raised to the caller.
Example 2: asyncio.shield()
await asyncio.wait_for(    asyncio.shield(task),    timeout=2)



Here, shield() protects the underlying task from cancellation caused by the timeout.

task = asyncio.create_task(fetch_api("API C", 5))

try:
    await asyncio.wait_for(task, timeout=2)

except TimeoutError:
    print("Timed out")

print("Task cancelled:", task.cancelled())

Method	Meaning
task.cancel()	Requests cancellation
task.cancelled()	Checks whether the task actually finished in a cancelled state
task.done()	Checks whether the task has finished, successfully, exceptionally, or by cancellation
"""