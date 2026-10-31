"""Командний інтерфейс для демонстрації лабораторної роботи."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

from core import Student, build_pipeline, reduce_stats


def load_students(path: Path) -> list[Student]:
    """Зчитує записи студентів із JSON-файлу."""
    with path.open("r", encoding="utf-8") as source:
        data = json.load(source)

    if not isinstance(data, list):
        raise ValueError("JSON повинен містити список студентів.")

    students: list[Student] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Кожен запис має бути JSON-об'єктом.")
        required = {"id", "name", "group", "lab_scores"}
        if not required.issubset(item):
            raise ValueError(f"У записі відсутні поля: {required - set(item)}")
        if not isinstance(item["lab_scores"], list):
            raise ValueError("Поле lab_scores повинно бути списком.")
        students.append(cast(Student, item))
    return students


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Аналіз результатів лабораторних робіт студентів."
    )
    parser.add_argument("--data", type=Path, default=Path("sample_data.json"))
    parser.add_argument(
        "--top", type=int, default=5, help="Кількість записів у рейтингу"
    )
    parser.add_argument("--bonus-group", default="ІПЗ-21")
    parser.add_argument("--bonus", type=float, default=5.0)
    parser.add_argument("--min-average", type=float, default=60.0)
    args = parser.parse_args()

    students = load_students(args.data)
    pipeline = build_pipeline(
        top_n=args.top,
        bonus_group=args.bonus_group,
        bonus=args.bonus,
        min_average=args.min_average,
    )
    result = pipeline(students)

    print("\nРЕЙТИНГ СТУДЕНТІВ")
    print("-" * 78)
    print(
        f"{'Місце':<7}{'ID':<6}{'Ім’я':<24}{'Група':<14}{'Сума':>10}{'Середній':>10}{'Фінал':>9}"
    )
    print("-" * 78)
    for place, student in enumerate(result, start=1):
        print(
            f"{place:<7}{student['id']:<6}{student['name']:<24}"
            f"{student['group']:<14}{student['total_score']:>10.2f}"
            f"{student['avg_score']:>10.2f}{student['final_score']:>9.2f}"
        )

    stats = reduce_stats(result)
    print("\nЗАГАЛЬНА СТАТИСТИКА ДЛЯ СФОРМОВАНОГО TOP-N")
    print(f"Кількість студентів: {int(stats['count'])}")
    print(f"Сума балів лабораторних: {stats['total_score']:.2f}")
    print(f"Середній бал: {stats['avg_score']:.2f}")


if __name__ == "__main__":
    main()
