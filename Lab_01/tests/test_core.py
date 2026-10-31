
from copy import deepcopy

import pytest

from core import (
    calculate_average,
    calculate_bonus,
    calculate_penalty,
    check_qualification,
    create_default_processor,
    make_processor
)


@pytest.fixture
def sample_athletes():
    return [
        {
            "id": 1,
            "name": "Олександр",
            "attempts": [60.0, 70.0, 80.0],
            "status": "completed",
            "category": "professional"
        },
        {
            "id": 2,
            "name": "Марія",
            "attempts": [40.0, 50.0, 60.0],
            "status": "completed",
            "category": "senior"
        },
        {
            "id": 3,
            "name": "Андрій",
            "attempts": [30.0, 40.0],
            "status": "disqualified",
            "category": "junior"
        }
    ]


# Тест 1. Перевірка агрегації
def test_calculate_average():
    assert calculate_average([60.0, 70.0, 80.0]) == 70.0
    assert calculate_average([]) == 0.0


# Тест 2. Перевірка бонусів
def test_calculate_bonus():
    assert calculate_bonus("junior") == 5.0
    assert calculate_bonus("senior") == 10.0
    assert calculate_bonus("professional") == 15.0
    assert calculate_bonus("unknown") == 0.0


# Тест 3. Перевірка штрафів
def test_calculate_penalty():
    athlete = {
        "id": 1,
        "name": "Тест",
        "attempts": [10.0, 20.0, 30.0],
        "status": "completed",
        "category": "junior"
    }

    assert calculate_penalty(athlete) == 0.0

    athlete_many_attempts = {
        **athlete,
        "attempts": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
    }

    assert calculate_penalty(athlete_many_attempts) == 5.0


# Тест 4. Перевірка кваліфікації
def test_check_qualification():
    assert check_qualification(75.0, "professional") is True
    assert check_qualification(50.0, "professional") is False
    assert check_qualification(40.0, "junior") is True


# Тест 5. Перевірка референтної прозорості
def test_referential_transparency(sample_athletes):
    processor = create_default_processor()

    result1 = processor(sample_athletes)
    result2 = processor(sample_athletes)

    assert result1 == result2


# Тест 6. Перевірка відсутності мутацій
def test_no_mutation(sample_athletes):
    processor = create_default_processor()

    original = deepcopy(sample_athletes)

    processor(sample_athletes)

    assert sample_athletes == original


# Тест 7. Перевірка фільтрації за статусом
def test_status_filter(sample_athletes):
    processor = create_default_processor()

    result = processor(sample_athletes)

    assert result["count"] == 2


# Тест 8. Перевірка Callable-політик
def test_callable_policies(sample_athletes):
    processor = make_processor(
        aggregate=lambda attempts: sum(attempts),
        apply_bonus=lambda category: 20.0,
        apply_penalty=lambda athlete: 0.0,
        qualify=lambda result, category: result >= 100
    )

    result = processor(sample_athletes)

    athletes = result["results"]

    assert athletes[0]["average_result"] == 210.0
    assert athletes[0]["bonus"] == 20.0
    assert athletes[0]["final_result"] == 230.0
    assert athletes[0]["qualified"] is True


# Тест 9. Перевірка створення нового результату
def test_new_result_does_not_modify_original(sample_athletes):
    processor = create_default_processor()

    result = processor(sample_athletes)

    assert "final_result" not in sample_athletes[0]
    assert "final_result" in result["results"][0]
    assert sample_athletes[0]["attempts"] is not result["results"][0]["attempts"]


# Тест 10. Перевірка порожнього списку
def test_empty_athletes():
    processor = create_default_processor()

    result = processor([])

    assert result["count"] == 0
    assert result["qualified_count"] == 0
    assert result["not_qualified_count"] == 0
    assert result["results"] == []
