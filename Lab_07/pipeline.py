"""Функціональний конвеєр обробки результатів лабораторних робіт."""
from __future__ import annotations

from functools import partial, reduce
from operator import itemgetter, methodcaller
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")


def pipeline(value: T, *funcs: Callable[[Any], Any]) -> Any:
    """Послідовно передає результат кожної функції наступній."""
    return reduce(lambda current, func: func(current), funcs, value)


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "так", "submitted"}:
        return True
    if normalized in {"false", "0", "no", "ні", "not submitted"}:
        return False
    raise ValueError(f"Некоректне значення submitted: {value!r}")


get_student = itemgetter("student")
get_lab = itemgetter("lab")
get_score = itemgetter("score")
strip_text = methodcaller("strip")
title_text = methodcaller("title")


def normalize_result(row: dict[str, Any]) -> dict[str, Any]:
    """Нормалізує типи та текст одного запису."""
    required = {"student", "lab", "score", "attempts", "submitted"}
    missing = required.difference(row)
    if missing:
        raise ValueError(f"У записі відсутні поля: {', '.join(sorted(missing))}")
    student = title_text(strip_text(str(get_student(row))))
    if not student:
        raise ValueError("Ім'я студента не може бути порожнім")
    lab = int(get_lab(row))
    score = float(get_score(row))
    attempts = int(row["attempts"])
    if lab < 1 or attempts < 1:
        raise ValueError("Номер лабораторної та кількість спроб мають бути додатними")
    if not 0 <= score <= 100:
        raise ValueError("Бал має бути в діапазоні від 0 до 100")
    return {"student": student, "lab": lab, "score": score,
            "attempts": attempts, "submitted": _to_bool(row["submitted"])}


def final_score(row: dict[str, Any], penalty: float = 0.5) -> dict[str, Any]:
    """Рахує підсумковий бал: мінус penalty за кожну спробу після першої."""
    result = dict(row)
    result["final_score"] = round(max(0.0, result["score"] - (result["attempts"] - 1) * penalty), 2)
    return result


def map_with(function: Callable[[Any], Any]) -> Callable[[Iterable[Any]], map]:
    return partial(map, function)


def filter_with(predicate: Callable[[Any], bool]) -> Callable[[Iterable[Any]], filter]:
    return partial(filter, predicate)


def take_top(count: int, rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if count < 0:
        raise ValueError("top не може бути від'ємним")
    return list(rows)[:count]


def clean_and_rank(source: object, top: int = 3, penalty: float = 0.5) -> list[dict[str, Any]]:
    """Завантажує, нормалізує, відбирає здані роботи та повертає Top-N."""
    from loaders import load_results

    if top < 0:
        raise ValueError("top не може бути від'ємним")
    normalize_stage = map_with(normalize_result)
    submitted_stage = filter_with(itemgetter("submitted"))
    score_stage = map_with(partial(final_score, penalty=penalty))
    sort_stage = partial(sorted, key=lambda row: (-row["final_score"], row["attempts"], row["student"].casefold()))
    top_stage = partial(take_top, top)
    return pipeline(load_results(source), normalize_stage, submitted_stage,
                    score_stage, list, sort_stage, top_stage)
