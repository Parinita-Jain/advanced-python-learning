
import time
from functools import wraps


def execution_timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print(f"{func.__name__} took {end - start:.4f} seconds")

        return result

    return wrapper


@execution_timer
def calculate_total(a, b):
    time.sleep(1)
    return a + b


@execution_timer
def greet(name, message="Hello"):
    time.sleep(0.5)
    return f"{message}, {name}!"


result1 = calculate_total(10, 20)
print("Result:", result1)

result2 = greet("Rahul", message="Welcome")
print("Result:", result2)


7