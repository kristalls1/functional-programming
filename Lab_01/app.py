
from core import create_default_processor


# Демонстраційні дані спортсменів
athletes = [
    {
        "id": 1,
        "name": "Олександр",
        "attempts": [65.0, 70.0, 75.0],
        "status": "completed",
        "category": "professional"
    },
    {
        "id": 2,
        "name": "Марія",
        "attempts": [40.0, 45.0, 50.0],
        "status": "completed",
        "category": "senior"
    },
    {
        "id": 3,
        "name": "Андрій",
        "attempts": [25.0, 30.0, 35.0],
        "status": "completed",
        "category": "junior"
    },
    {
        "id": 4,
        "name": "Софія",
        "attempts": [80.0, 85.0],
        "status": "disqualified",
        "category": "professional"
    },
    {
        "id": 5,
        "name": "Дмитро",
        "attempts": [35.0, 40.0, 45.0],
        "status": "completed",
        "category": "junior"
    }
]


# Функція виведення звіту
def render_report(result: dict[str, object]) -> None:
    print("\n" + "=" * 55)
    print("          РЕЗУЛЬТАТИ СПОРТИВНИХ ЗМАГАНЬ")
    print("=" * 55)

    print(f"\nОброблено спортсменів: {result['count']}")
    print(f"Кваліфіковано: {result['qualified_count']}")
    print(f"Не кваліфіковано: {result['not_qualified_count']}")

    print("\nДетальні результати:")
    print("-" * 55)

    for athlete in result["results"]:
        print(f"\nID: {athlete['id']}")
        print(f"Ім'я: {athlete['name']}")
        print(f"Категорія: {athlete['category']}")
        print(f"Спроби: {athlete['attempts']}")
        print(f"Середній результат: {athlete['average_result']:.2f}")
        print(f"Бонус: +{athlete['bonus']:.2f}")
        print(f"Штраф: -{athlete['penalty']:.2f}")
        print(f"Підсумковий результат: {athlete['final_result']:.2f}")

        if athlete["qualified"]:
            print("Кваліфікація: ПРОЙШОВ")
        else:
            print("Кваліфікація: НЕ ПРОЙШОВ")

    print("\n" + "=" * 55)


def main() -> None:
    processor = create_default_processor()

    result = processor(athletes)

    render_report(result)


if __name__ == "__main__":
    main()
