"""Рекурсивні та ітеративні алгоритми для задачі про рюкзак 0/1."""
from __future__ import annotations

from functools import lru_cache
from typing import Protocol, TypeAlias

Item: TypeAlias = tuple[int, int]  # (вага, цінність)


class CacheStatistics(Protocol):
    """Поля статистики, які повертає functools.lru_cache."""

    @property
    def hits(self) -> int: ...

    @property
    def misses(self) -> int: ...

    @property
    def maxsize(self) -> int | None: ...

    @property
    def currsize(self) -> int: ...


def _validate(items: tuple[Item, ...], capacity: int) -> None:
    """Перевіряє вхідні дані та не допускає неоднозначних значень."""
    if isinstance(capacity, bool) or not isinstance(capacity, int):
        raise TypeError("Місткість рюкзака має бути цілим числом.")
    if capacity < 0:
        raise ValueError("Місткість рюкзака не може бути від'ємною.")
    for index, item in enumerate(items):
        if not isinstance(item, tuple) or len(item) != 2:
            raise TypeError(f"Предмет {index} має бути парою (вага, цінність).")
        weight, value = item
        if isinstance(weight, bool) or not isinstance(weight, int):
            raise TypeError("Вага предмета має бути цілим числом.")
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Цінність предмета має бути цілим числом.")
        if weight <= 0:
            raise ValueError("Вага кожного предмета має бути більшою за нуль.")
        if value < 0:
            raise ValueError("Цінність предмета не може бути від'ємною.")


def knapsack_recursive(items: tuple[Item, ...], capacity: int) -> int:
    """Наївне рекурсивне розв'язання без мемоізації."""
    normalized = tuple(items)
    _validate(normalized, capacity)

    def solve(index: int, remaining: int) -> int:
        if index == len(normalized) or remaining == 0:
            return 0
        weight, value = normalized[index]
        if weight > remaining:
            return solve(index + 1, remaining)
        return max(
            solve(index + 1, remaining),
            value + solve(index + 1, remaining - weight),
        )

    return solve(0, capacity)


class KnapsackSolver:
    """Мемоізований розв'язувач; ключ кешу — (index, capacity)."""

    def __init__(self, items: tuple[Item, ...], capacity: int) -> None:
        self.items = tuple(items)
        _validate(self.items, capacity)
        self.capacity = capacity

    @lru_cache(maxsize=None)
    def _solve(self, index: int, remaining: int) -> int:
        if index == len(self.items) or remaining == 0:
            return 0
        weight, value = self.items[index]
        if weight > remaining:
            return self._solve(index + 1, remaining)
        return max(
            self._solve(index + 1, remaining),
            value + self._solve(index + 1, remaining - weight),
        )

    def solve(self) -> int:
        """Повертає максимальну сумарну цінність предметів."""
        return self._solve(0, self.capacity)

    def cache_info(self) -> CacheStatistics:
        """Повертає статистику кешу functools.lru_cache."""
        return self._solve.cache_info()

    def cache_clear(self) -> None:
        """Очищає кеш мемоізованих станів."""
        self._solve.cache_clear()


def knapsack_memoized(items: tuple[Item, ...], capacity: int) -> int:
    """Зручна функція-обгортка для мемоізованого розв'язання."""
    return KnapsackSolver(tuple(items), capacity).solve()


def knapsack_iterative(items: tuple[Item, ...], capacity: int) -> int:
    """Ітеративне DP-рішення з одновимірним масивом."""
    normalized = tuple(items)
    _validate(normalized, capacity)
    dp = [0] * (capacity + 1)
    for weight, value in normalized:
        for current_capacity in range(capacity, weight - 1, -1):
            dp[current_capacity] = max(
                dp[current_capacity],
                value + dp[current_capacity - weight],
            )
    return dp[capacity]


def example_items() -> tuple[Item, ...]:
    """Повертає набір предметів для демонстрації."""
    return ((2, 12), (1, 10), (3, 20), (2, 15), (4, 25))
