"""Консольна демонстрація задачі про рюкзак 0/1."""
from __future__ import annotations

from algorithms import (
    KnapsackSolver,
    example_items,
    knapsack_iterative,
    knapsack_recursive,
)


def print_items(items: tuple[tuple[int, int], ...]) -> None:
    print("\nПредмети (номер: вага, цінність):")
    for number, (weight, value) in enumerate(items, start=1):
        print(f"{number}: вага = {weight}, цінність = {value}")


def main() -> None:
    items = example_items()
    capacity = 5
    solver = KnapsackSolver(items, capacity)

    while True:
        print("\n=== Задача про рюкзак 0/1 — варіант 15 ===")
        print("1. Показати предмети та місткість")
        print("2. Розв'язати рекурсивно без кешу")
        print("3. Розв'язати рекурсивно з lru_cache")
        print("4. Розв'язати ітеративно")
        print("5. Показати статистику кешу")
        print("6. Очистити кеш")
        print("0. Вихід")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            print_items(items)
            print(f"Місткість рюкзака: {capacity}")
        elif choice == "2":
            print(f"Максимальна цінність: {knapsack_recursive(items, capacity)}")
        elif choice == "3":
            print(f"Максимальна цінність: {solver.solve()}")
        elif choice == "4":
            print(f"Максимальна цінність: {knapsack_iterative(items, capacity)}")
        elif choice == "5":
            print(f"Статистика кешу: {solver.cache_info()}")
        elif choice == "6":
            solver.cache_clear()
            print("Кеш очищено.")
        elif choice == "0":
            print("Роботу завершено.")
            break
        else:
            print("Невідомий пункт меню. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
