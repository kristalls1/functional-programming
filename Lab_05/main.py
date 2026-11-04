"""Демонстрація варіанта 15 — потік вимірювань через callable."""
from itertools import islice
from streams import (
    bounded_measurements, moving_average, prefix_statistics, prefix_sums,
    sliding_window, take, drop,
)


class DemoProvider:
    """Детермінований постачальник для відтворюваної демонстрації."""
    def __init__(self, values: list[float], sentinel=None):
        self._values = iter(values)
        self._sentinel = sentinel

    def __call__(self):
        return next(self._values, self._sentinel)


def main() -> None:
    raw_values = [21.0, 22.5, 999.0, 23.0, 24.5, -100.0, 25.0, 26.0, 27.5]
    provider = DemoProvider(raw_values)
    stream = bounded_measurements(provider)

    print("=== Лабораторна робота 5 — варіант 15 ===")
    print("Вихідний набір:", raw_values)
    print("1. Допустимі вимірювання:", take(20, stream))

    filtered = [21.0, 22.5, 23.0, 24.5, 25.0, 26.0, 27.5]
    print("2. Рухоме середнє (вікно 3):", list(moving_average(filtered, 3)))
    print("3. Префіксні суми:", list(prefix_sums(filtered)))
    print("4. Префіксна статистика (кількість, сума, середнє):")
    for row in prefix_statistics(filtered):
        print("  ", row)
    print("5. Друге та наступні вікна:", list(islice(drop(1, sliding_window(filtered, 3)), 3)))


if __name__ == "__main__":
    main()
