# Лабораторна робота №2 — варіант 15

**Тема:** Функції вищого порядку, lambda та композиція.  
**Предметна область:** результати лабораторних робіт студентів.

## Призначення

Програма зчитує список студентів із JSON, обчислює суму та середній бал лабораторних робіт, додає бонус студентам заданої групи, відбирає допущених до рейтингу та формує Top-N. Початкові записи не змінюються: кожна трансформація створює новий словник.

## Структура проєкту

```text
functional-programming/
└── Lab_02/
    ├── main.py
    ├── core.py
    ├── app.py
    ├── README.md
    ├── ASSIGNMENT.md
    ├── requirements.txt
    ├── pyproject.toml
    ├── sample_data.json
    ├── tests/
    │   └── test_core.py
    └── report/
        ├── Lab_02_15.pdf
        └── Lab_02_15_final_screenshots.docx
```

## Встановлення та запуск (Windows PowerShell)

Перейдіть у папку `Lab_02`:

```powershell
cd Lab_02
py -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

Запуск програми через головний файл:

```powershell
python main.py --data sample_data.json --top 3
```

Також можна запустити CLI-модуль безпосередньо:

```powershell
python app.py --data sample_data.json --top 3
```

Приклад із власними параметрами:

```powershell
python main.py --data sample_data.json --top 4 --bonus-group "ІПЗ-22" --bonus 7 --min-average 65
```

## Параметри

| Параметр | Призначення | Значення за замовчуванням |
|---|---|---:|
| `--data` | Шлях до JSON-файлу | `sample_data.json` |
| `--top` | Кількість записів у рейтингу | `5` |
| `--bonus-group` | Група, якій нараховується бонус | `ІПЗ-21` |
| `--bonus` | Бонус до середнього бала | `5` |
| `--min-average` | Мінімальний середній бал для допуску | `60` |

## Логіка обчислень

1. `normalize_names()` нормалізує відображення імен.
2. `with_score_statistics()` обчислює `total_score` та `avg_score`.
3. `apply_group_bonus()` додає бонус до середнього бала вибраної групи. Підсумковий бал обмежується значенням 100.
4. `only_admitted()` залишає студентів із середнім балом не нижче порога.
5. `sort_and_take()` сортує за `final_score` за спаданням, а при однаковому результаті — за `id` за зростанням, після чого бере Top-N.
6. `reduce_stats()` окремо обчислює кількість записів, суму балів лабораторних і середній бал для сформованого Top-N.

## Перевірки якості

```powershell
pytest -q
black --check .
ruff check .
mypy core.py app.py main.py tests
```
