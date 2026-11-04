"""Поліморфне завантаження результатів лабораторних робіт."""
from __future__ import annotations

import csv
import io
import json
from functools import singledispatch
from pathlib import Path
from typing import Any

Record = dict[str, Any]


def _load_text(text: str, suffix: str = "") -> list[Record]:
    """Розбирає JSON або CSV-текст залежно від розширення джерела."""
    if suffix.lower() == ".csv":
        return [dict(row) for row in csv.DictReader(io.StringIO(text))]
    parsed = json.loads(text)
    if not isinstance(parsed, list) or any(not isinstance(row, dict) for row in parsed):
        raise ValueError("Очікується JSON-масив об'єктів")
    return parsed


@singledispatch
def load_results(source: object) -> list[Record]:
    """Завантажує записи з підтримуваного джерела."""
    raise TypeError(f"Непідтримуваний тип джерела: {type(source)!r}")


@load_results.register(str)
def _(source: str) -> list[Record]:
    stripped = source.strip()
    if stripped.startswith("["):
        return _load_text(stripped)
    path = Path(source)
    return _load_text(path.read_text(encoding="utf-8"), path.suffix)


@load_results.register(Path)
def _(source: Path) -> list[Record]:
    return _load_text(source.read_text(encoding="utf-8"), source.suffix)


@load_results.register(io.TextIOBase)
def _(source: io.TextIOBase) -> list[Record]:
    name = getattr(source, "name", "")
    return _load_text(source.read(), Path(str(name)).suffix)


@load_results.register(list)
def _(source: list) -> list[Record]:
    if any(not isinstance(row, dict) for row in source):
        raise ValueError("Очікується список словників")
    return [dict(row) for row in source]

