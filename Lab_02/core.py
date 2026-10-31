

from __future__ import annotations

from functools import reduce
from itertools import islice
from typing import Any, Callable, Iterable, Iterator, TypedDict, cast

from typing_extensions import NotRequired


class Student(TypedDict):
   

    id: int
    name: str
    group: str
    lab_scores: list[float]
    total_score: NotRequired[float]
    avg_score: NotRequired[float]
    final_score: NotRequired[float]


Stats = dict[str, float]
Transform = Callable[[Iterable[Student]], Iterable[Student]]


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    

    def composed(value: Any) -> Any:
        result = value
        for function in reversed(functions):
            result = function(result)
        return result

    return composed


def with_score_statistics() -> Transform:
    

    def transform(students: Iterable[Student]) -> Iterator[Student]:
        for student in students:
            scores = student["lab_scores"]
            total = float(sum(scores))
            average = total / len(scores) if scores else 0.0
            yield {
                **student,
                "total_score": total,
                "avg_score": average,
                "final_score": average,
            }

    return transform


def apply_group_bonus(group: str, bonus: float) -> Transform:
    

    def transform(students: Iterable[Student]) -> Iterator[Student]:
        for student in students:
            current = float(student.get("avg_score", 0.0))
            final = (
                min(100.0, current + bonus) if student["group"] == group else current
            )
            yield {**student, "final_score": final}

    return transform


def only_admitted(min_average: float) -> Transform:
    
    return lambda students: (
        student
        for student in students
        if float(student.get("avg_score", 0.0)) >= min_average
    )


def normalize_names() -> Transform:
    return lambda students: (
        {**student, "name": student["name"].strip().title()} for student in students
    )


def sort_and_take(top_n: int) -> Transform:
    def transform(students: Iterable[Student]) -> list[Student]:
        ordered = sorted(
            students,
            key=lambda student: (
                -float(student.get("final_score", 0.0)),
                student["id"],
            ),
        )
        return list(islice(ordered, max(0, top_n)))

    return transform


def build_pipeline(
    top_n: int = 5,
    bonus_group: str = "ІПЗ-21",
    bonus: float = 5.0,
    min_average: float = 60.0,
) -> Callable[[Iterable[Student]], list[Student]]:
    pipeline = compose(
        sort_and_take(top_n),
        only_admitted(min_average),
        apply_group_bonus(bonus_group, bonus),
        with_score_statistics(),
        normalize_names(),
    )
    return cast(Callable[[Iterable[Student]], list[Student]], pipeline)


def reduce_stats(students: Iterable[Student]) -> Stats:
    initial: Stats = {"count": 0.0, "total_score": 0.0, "avg_score_sum": 0.0}
    accumulated = reduce(
        lambda acc, student: {
            "count": acc["count"] + 1.0,
            "total_score": acc["total_score"] + float(student.get("total_score", 0.0)),
            "avg_score_sum": acc["avg_score_sum"]
            + float(student.get("avg_score", 0.0)),
        },
        students,
        initial,
    )
    count = accumulated["count"]
    return {
        "count": count,
        "total_score": accumulated["total_score"],
        "avg_score": accumulated["avg_score_sum"] / count if count else 0.0,
    }
