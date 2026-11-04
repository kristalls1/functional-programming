"""Єдина точка входу для демонстрації лабораторної роботи №7, варіант 15."""
from __future__ import annotations
import json
from pathlib import Path
from operator import attrgetter, itemgetter, methodcaller
from loaders import load_results
from models import LabResult
from pipeline import clean_and_rank, pipeline

BASE = Path(__file__).parent


def main() -> None:
    json_path = BASE / "sample_data.json"
    csv_path = BASE / "sample_data.csv"
    print("Лабораторна робота №7 — варіант 15")
    print("Top-3 зданих лабораторних робіт:")
    for number, row in enumerate(clean_and_rank(json_path, top=3), start=1):
        print(f"{number}. {row['student']}: {row['final_score']} балів; "
              f"спроб: {row['attempts']}; лабораторна №{row['lab']}")

    print("\nЗавантаження CSV через singledispatch:")
    print(f"Кількість записів: {len(load_results(csv_path))}")

    print("\nПорівняння об'єктів LabResult:")
    results = [LabResult("Alice", 1, 87, 2), LabResult("Bob", 1, 93, 1),
               LabResult("Carol", 1, 93, 2)]
    print(sorted(results, key=attrgetter("score"), reverse=True))
    print(f"Найкращий результат: {max(results)}")


if __name__ == "__main__":
    main()
