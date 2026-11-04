# Вимоги варіанта 15 та відповідність

- Предметна область: результати лабораторних робіт; поля student, lab, score, attempts, submitted.
- Відбір зданих робіт, нормалізація, підсумковий бал, Top-N — `pipeline.py`.
- `pipeline` реалізовано через `reduce`; `partial` застосовано для налаштування map/filter/sort/top та штрафу.
- `load_results` через `singledispatch`: str, Path, відкритий файл, list; JSON і CSV.
- `LabResult` з `total_ordering`, `__eq__`, `__lt__`, `NotImplemented`.
- Використано `itemgetter`, `attrgetter`, `methodcaller`.
- pytest-тести охоплюють функції, джерела даних, валідацію та порівняння.
