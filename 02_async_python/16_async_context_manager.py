"""
Objective: Learn how async with works and how Python performs asynchronous setup and cleanup using __aenter__() and __aexit__().
"""


import asyncio


class DatabaseConnection:

    async def __aenter__(self):
        print("Connecting to database...")
        await asyncio.sleep(1)
        print("Database connected.")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        print("Closing database connection...")
        await asyncio.sleep(1)
        print("Database connection closed.")

    async def fetch_data(self):
        print("Fetching data...")
        await asyncio.sleep(2)
        print("Data fetched successfully.")
        return ["Employee 1", "Employee 2"]


async def main():

    async with DatabaseConnection() as db:
        """
        data = await db.fetch_data()
        print("Result:", data)
        """
        raise ValueError("Something went wrong!")


asyncio.run(main())

"""
Suppose an exception occurs inside an async with block. In that case, Python will still call the __aexit__() method to perform 
cleanup, and it will pass the exception details to __aexit__() so that you can handle it appropriately.

i.e. __aexit__() executes, performs cleanup, and the exception propagates unless explicitly suppressed.
"""
