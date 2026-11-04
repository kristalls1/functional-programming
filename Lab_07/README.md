# Лабораторна робота №7 — варіант 15

**Тема:** `functools` та `operator`. **Предметна область:** результати лабораторних робіт студентів.

## Реалізація
- `pipeline(value, *funcs)` послідовно виконує функції за допомогою `functools.reduce`.
- `clean_and_rank(source, top=3)` завантажує записи, нормалізує поля `student`, `lab`, `score`, `attempts`, `submitted`, залишає лише здані роботи, рахує підсумковий бал і формує Top-N.
- Підсумковий бал: `score - 0.5 × (attempts - 1)`, але не нижче нуля. Це явно визначена політика оцінювання для демонстрації обчислення.
- `load_results` використовує `singledispatch` і підтримує JSON-рядок, шлях `str`, `Path`, відкритий текстовий файл та список словників; файлові джерела підтримують JSON і CSV.
- `LabResult` використовує `@total_ordering`; порядок визначається балом, меншою кількістю спроб та іменем студента.
- Застосовано `partial`, `reduce`, `itemgetter`, `attrgetter` і `methodcaller`.

## Запуск
```bash
python -m pip install -r requirements.txt
python lab07.py
pytest -q
```

## Перевірки стилю та типів
```bash
black --check .
ruff check .
mypy .
```

## Структура
`loaders.py` — поліморфне завантаження; `pipeline.py` — конвеєр; `models.py` — модель порівняння; `lab07.py` — демонстрація; `tests/` — автоматичні тести.
