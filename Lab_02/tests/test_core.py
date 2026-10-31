from copy import deepcopy
from typing import Any, cast

from core import (
    Student,
    apply_group_bonus,
    build_pipeline,
    compose,
    reduce_stats,
    sort_and_take,
    with_score_statistics,
)


def sample_students() -> list[Student]:
    return [
        {"id": 3, "name": "анна мельник", "group": "А", "lab_scores": [90, 90]},
        {"id": 1, "name": "іван бондар", "group": "Б", "lab_scores": [80, 80]},
        {"id": 2, "name": "олена коваль", "group": "А", "lab_scores": [90, 90]},
        {"id": 4, "name": "петро", "group": "Б", "lab_scores": [40, 40]},
    ]


def test_top_n_and_two_sort_keys() -> None:
    students = list(with_score_statistics()(sample_students()))
    result = sort_and_take(2)(students)
    assert [student["id"] for student in result] == [2, 3]


def test_input_records_are_not_mutated() -> None:
    students = sample_students()
    original = deepcopy(students)
    list(with_score_statistics()(students))
    assert students == original


def test_group_bonus_is_applied_only_to_selected_group() -> None:
    prepared = list(with_score_statistics()(sample_students()))
    result = list(apply_group_bonus("А", 5)(prepared))
    by_id = {student["id"]: student for student in result}
    assert by_id[2]["final_score"] == 95
    assert by_id[1]["final_score"] == 80


def test_reduce_stats() -> None:
    prepared = list(with_score_statistics()(sample_students()[:2]))
    stats = reduce_stats(prepared)
    assert stats["count"] == 2
    assert stats["total_score"] == 340
    assert stats["avg_score"] == 85


def test_compose_applies_functions_right_to_left() -> None:
    pipeline = compose(
        cast(Any, lambda value: value + 3),
        cast(Any, lambda value: value * 2),
    )
    assert pipeline(4) == 11


def test_full_pipeline_filters_and_limits_results() -> None:
    result = build_pipeline(top_n=2, bonus_group="А", bonus=5, min_average=60)(
        sample_students()
    )
    assert isinstance(result, list)
    assert [student["id"] for student in result] == [2, 3]
