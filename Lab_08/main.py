from __future__ import annotations
from evaluator import eval_query
from model import And, Eq, Field, Not, Or
from pretty import render_query
def main() -> None:
    records: list[dict[str, object]] = [
        {"name": "Anna", "age": 20, "city": "Lviv", "active": True},
        {"name": "Oleh", "age": 17, "city": "Kyiv", "active": True},
        {"name": "Iryna", "age": 22, "city": "Lviv", "active": False},
        {"name": "Mark", "age": 19, "city": "Odesa", "active": True},
        {"name": "Sofiia", "age": 19, "city": "Lviv", "active": True},
    ]
    query = And(Eq(Field("city"), "Lviv"),
                And(Eq(Field("active"), True),
                    Not(Or(Eq(Field("age"), 20), Eq(Field("age"), 22)))))
    print("Запит:", render_query(query))
    print("\nРезультати фільтрації:")
    for record in records:
        if eval_query(query, record):
            print(f"- {record['name']}: {record}")
if __name__ == "__main__":
    main()
