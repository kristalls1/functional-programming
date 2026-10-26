
from typing import TypedDict, Callable, Iterable


class Athlete(TypedDict):
    id: int
    name: str
    attempts: list[float]
    status: str
    category: str


class AthleteResult(Athlete, total=False):
    average_result: float
    bonus: float
    penalty: float
    final_result: float
    qualified: bool


# Типи функцій для передачі політик
AggregationFn = Callable[[list[float]], float]
BonusFn = Callable[[str], float]
PenaltyFn = Callable[[Athlete], float]
QualificationFn = Callable[[float, str], bool]


# 1. Обчислення середнього результату спроб
def calculate_average(attempts: list[float]) -> float:
    if not attempts:
        return 0.0

    return sum(attempts) / len(attempts)


# 2. Отримання бонусу залежно від категорії
def calculate_bonus(category: str) -> float:
    bonuses = {
        "junior": 5.0,
        "senior": 10.0,
        "professional": 15.0
    }

    return bonuses.get(category, 0.0)


# 3. Обчислення штрафу залежно від кількості спроб
def calculate_penalty(athlete: Athlete) -> float:
    attempts_count = len(athlete["attempts"])

    if attempts_count > 5:
        return 5.0

    if attempts_count == 0:
        return 10.0

    return 0.0


# 4. Перевірка кваліфікації спортсмена
def check_qualification(
    final_result: float,
    category: str
) -> bool:
    minimum_results = {
        "junior": 30.0,
        "senior": 50.0,
        "professional": 70.0
    }

    minimum = minimum_results.get(category, 50.0)

    return final_result >= minimum


# 5. Створення нового запису з результатами
def create_result(
    athlete: Athlete,
    average: float,
    bonus: float,
    penalty: float,
    final_result: float,
    qualified: bool
) -> AthleteResult:

    return {
        **athlete,
        "attempts": list(athlete["attempts"]),
        "average_result": average,
        "bonus": bonus,
        "penalty": penalty,
        "final_result": final_result,
        "qualified": qualified
    }


# 6. Функція вищого порядку — фабрика обробника
def make_processor(
    *,
    aggregate: AggregationFn,
    apply_bonus: BonusFn,
    apply_penalty: PenaltyFn,
    qualify: QualificationFn
) -> Callable[[Iterable[Athlete]], dict[str, object]]:

    def process(
        athletes: Iterable[Athlete]
    ) -> dict[str, object]:

        results = []

        for athlete in athletes:

            # Обробляємо тільки завершені виступи
            if athlete["status"] != "completed":
                continue

            average = aggregate(athlete["attempts"])

            bonus = apply_bonus(athlete["category"])

            penalty = apply_penalty(athlete)

            final_result = average + bonus - penalty

            qualified = qualify(
                final_result,
                athlete["category"]
            )

            new_athlete = create_result(
                athlete,
                average,
                bonus,
                penalty,
                final_result,
                qualified
            )

            results.append(new_athlete)

        qualified_count = sum(
            1 for athlete in results if athlete["qualified"]
        )

        return {
            "count": len(results),
            "qualified_count": qualified_count,
            "not_qualified_count": len(results) - qualified_count,
            "results": results
        }

    return process


# 7. Створення стандартного обробника
def create_default_processor() -> Callable:
    return make_processor(
        aggregate=calculate_average,
        apply_bonus=calculate_bonus,
        apply_penalty=calculate_penalty,
        qualify=check_qualification
    )
