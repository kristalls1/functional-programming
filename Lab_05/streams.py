"""Лінива обробка потоку вимірювань через ін'єкцію callable-постачальника."""
from __future__ import annotations

from collections import deque
from itertools import accumulate, count, islice, takewhile, dropwhile
from typing import Callable, Iterable, Iterator, TypeVar

T = TypeVar("T")


def measurement_stream(provider: Callable[[], float], sentinel: object = None) -> Iterator[float]:
    """Повертає вимірювання від callable-постачальника до sentinel."""
    for value in iter(provider, sentinel):
        yield float(value)


def valid_measurements(
    source: Iterable[float], minimum: float = -50.0, maximum: float = 150.0
) -> Iterator[float]:
    """Ліниво пропускає значення поза допустимим діапазоном."""
    if minimum > maximum:
        raise ValueError("Мінімальна межа не може перевищувати максимальну.")
    for value in source:
        if minimum <= value <= maximum:
            yield value


def take(n: int, source: Iterable[T]) -> list[T]:
    """Повертає перші n елементів ітератора."""
    if n < 0:
        raise ValueError("n не може бути від'ємним.")
    return list(islice(source, n))


def drop(n: int, source: Iterable[T]) -> Iterator[T]:
    """Ліниво пропускає перші n елементів."""
    if n < 0:
        raise ValueError("n не може бути від'ємним.")
    iterator = iter(source)
    next(islice(iterator, n, n), None)
    return iterator


def sliding_window(source: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    """Створює послідовні вікна розміру k без матеріалізації всього потоку."""
    if k <= 0:
        raise ValueError("Розмір вікна k має бути додатним.")
    iterator = iter(source)
    window: deque[T] = deque(maxlen=k)
    for _ in range(k):
        try:
            window.append(next(iterator))
        except StopIteration:
            return
    yield tuple(window)
    for value in iterator:
        window.append(value)
        yield tuple(window)


def moving_average(source: Iterable[float], k: int) -> Iterator[float]:
    """Обчислює рухоме середнє для кожного вікна."""
    for window in sliding_window(source, k):
        yield sum(window) / k


def prefix_statistics(source: Iterable[float]) -> Iterator[tuple[int, float, float]]:
    """Для кожного префікса повертає (кількість, суму, середнє)."""
    total = 0.0
    for number, value in zip(count(1), source):
        total += value
        yield number, total, total / number


def bounded_measurements(
    provider: Callable[[], float],
    sentinel: object = None,
    minimum: float = -50.0,
    maximum: float = 150.0,
) -> Iterator[float]:
    """Повний лінивий конвеєр отримання та фільтрації вимірювань."""
    yield from valid_measurements(
        measurement_stream(provider, sentinel), minimum, maximum
    )


def prefix_sums(source: Iterable[float]) -> Iterator[float]:
    """Префіксні суми на основі itertools.accumulate."""
    yield from accumulate(source)


def below_threshold(source: Iterable[float], threshold: float) -> Iterator[float]:
    """Повертає початкову ділянку потоку, доки значення не перевищать поріг."""
    yield from takewhile(lambda value: value <= threshold, source)


def after_threshold(source: Iterable[float], threshold: float) -> Iterator[float]:
    """Пропускає початкові значення, що не перевищують поріг."""
    yield from dropwhile(lambda value: value <= threshold, source)
