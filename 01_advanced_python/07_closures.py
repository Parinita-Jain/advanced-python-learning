"""
Objective: Build a counter factory that creates multiple independent counters. 
Each counter should remember its own value even after the outer function has finished executing.

"""


def counter_factory():

    count = 0

    def counter():

        nonlocal count

        count += 1

        return count

    return counter


# Create two independent counters
counter1 = counter_factory()
counter2 = counter_factory()


# Use the first counter
print("Counter 1:", counter1())
print("Counter 1:", counter1())
print("Counter 1:", counter1())

# Use the second counter
print("Counter 2:", counter2())
print("Counter 2:", counter2())

# Use the first counter again
print("Counter 1:", counter1())
