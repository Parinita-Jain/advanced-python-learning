
import time
from concurrent.futures import ProcessPoolExecutor


def calculate_sum_of_squares(numbers):

    total = 0

    for number in numbers:
        total += number * number

    return total


def create_ranges():

    return [
        range(1, 2_000_001),
        range(2_000_001, 4_000_001),
        range(4_000_001, 6_000_001),
        range(6_000_001, 8_000_001)
    ]

def sequential_calculation(ranges):

    results = []

    for numbers in ranges:
        results.append(calculate_sum_of_squares(numbers))

    return results

def main():

    ranges = create_ranges()

    start = time.perf_counter()

    results = sequential_calculation(ranges)

    print(f"Sequential time: {time.perf_counter() - start:.2f} seconds")

    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=4) as executor:
        parallel_results = list(
            executor.map(calculate_sum_of_squares, ranges)
        )

    print(f"Parallel time: {time.perf_counter() - start:.2f} seconds")

    print(f"Results match: {results == parallel_results}")

if __name__ == "__main__":
    main()  