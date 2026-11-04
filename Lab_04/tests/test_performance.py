"""Невеликий benchmark для порівняння реалізацій."""
from timeit import timeit

from algorithms import (
    KnapsackSolver,
    knapsack_iterative,
    knapsack_recursive,
)


def test_performance_comparison():
    items = tuple((index % 7 + 1, index % 13 + 3) for index in range(22))
    capacity = 35

    recursive_time = timeit(
        lambda: knapsack_recursive(items, capacity), number=3
    )
    memoized_time = timeit(
        lambda: KnapsackSolver(items, capacity).solve(), number=3
    )
    iterative_time = timeit(
        lambda: knapsack_iterative(items, capacity), number=3
    )

    assert knapsack_recursive(items, capacity) == knapsack_iterative(
        items, capacity
    )
    assert recursive_time > 0
    assert memoized_time > 0
    assert iterative_time > 0
