"""Тести алгоритмів задачі про рюкзак 0/1."""
import pytest

from algorithms import (
    KnapsackSolver,
    knapsack_iterative,
    knapsack_memoized,
    knapsack_recursive,
)


@pytest.mark.parametrize(
    "items, capacity, expected",
    [
        ((), 10, 0),
        (((2, 10),), 0, 0),
        (((2, 10),), 2, 10),
        (((3, 10), (4, 12)), 2, 0),
        (((2, 12), (1, 10), (3, 20), (2, 15)), 5, 37),
        (((1, 5), (1, 6), (1, 7)), 2, 13),
    ],
)
def test_all_implementations(items, capacity, expected):
    assert knapsack_recursive(items, capacity) == expected
    assert knapsack_memoized(items, capacity) == expected
    assert knapsack_iterative(items, capacity) == expected


def test_each_item_can_be_used_only_once():
    items = ((2, 10),)
    assert knapsack_iterative(items, 4) == 10


def test_memoization_records_cache_hits():
    solver = KnapsackSolver(((1, 2), (2, 4), (3, 5)), 3)
    solver.solve()
    info = solver.cache_info()
    assert info.misses > 0
    assert info.currsize > 0


def test_cache_clear_resets_statistics():
    solver = KnapsackSolver(((1, 2), (2, 4)), 2)
    solver.solve()
    solver.cache_clear()
    assert solver.cache_info().currsize == 0
    assert solver.cache_info().hits == 0


def test_input_is_not_mutated():
    items = ((2, 10), (1, 5))
    original = items[:]
    knapsack_recursive(items, 2)
    knapsack_memoized(items, 2)
    knapsack_iterative(items, 2)
    assert items == original


@pytest.mark.parametrize("capacity", [-1, 1.5, True])
def test_invalid_capacity(capacity):
    with pytest.raises((TypeError, ValueError)):
        knapsack_iterative(((1, 2),), capacity)


@pytest.mark.parametrize("items", [((0, 5),), ((-1, 5),), ((1, -5),)])
def test_invalid_items(items):
    with pytest.raises(ValueError):
        knapsack_iterative(items, 5)


def test_item_structure_validation():
    with pytest.raises(TypeError):
        knapsack_iterative(((1, 2, 3),), 5)
