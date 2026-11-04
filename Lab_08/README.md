# Лабораторна робота №8 — варіант 15
## Тема
Абстрактне дерево запитів: `Field`, `Eq`, `And`, `Or`, `Not`.

Реалізовано незмінні dataclass-вузли, рекурсивний `Query` через `Union`/`TypeAlias`, `Literal` для операторів, `Protocol` `SupportsRecordLookup`, чисті `eval_query()` і `render_query()` з `match/case`, а також помилку `QueryEvaluationError` для відсутнього поля.

## Структура
`model.py`, `evaluator.py`, `pretty.py`, `main.py`, `tests/test_query.py`, `mypy.ini`, `pyproject.toml`.

## Запуск
```bash
python -m pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
```
