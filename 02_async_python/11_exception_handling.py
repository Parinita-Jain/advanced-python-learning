
import asyncio


async def fetch_api(api_name, duration, should_fail=False):

    print(f"{api_name}: Started")

    await asyncio.sleep(duration)

    if should_fail:
        raise ValueError(f"{api_name} failed!")

    print(f"{api_name}: Completed")

    return f"{api_name} data"


async def main():

    results = await asyncio.gather(
        fetch_api("User API", 2),
        fetch_api("Payment API", 1, should_fail=True),
        fetch_api("Product API", 3),
        return_exceptions=True
    )

    print("\nProcessing results:")

    for result in results:

        if isinstance(result, Exception):
            print("Error:", result)

        else:
            print("Success:", result)


asyncio.run(main())
