# Лабораторна робота 5 — варіант 15

## Тема
Потік випадкових вимірювань через інжекцію callable-постачальника.

## Реалізація
`measurement_stream()` отримує значення через `iter(provider, sentinel)` і віддає їх генератором. `valid_measurements()` ліниво відкидає значення поза заданим діапазоном. Реалізовано `take`, `drop`, `sliding_window`, `moving_average`, префіксні суми через `itertools.accumulate` та префіксну статистику. Для потокової нумерації використовується `itertools.count`, а обмеження обсягу — `itertools.islice`.

## Запуск (Windows)
```powershell
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
pytest -q
python main.py
```

## Перевірки якості
```powershell
mypy .
black --check .
ruff check .
```

Постачальник у тестах детермінований: це дає змогу перевіряти результати без залежності від випадкового генератора. Усі потоки обробляються ліниво; скінченні списки створюються лише для демонстраційного виведення та тестів.
