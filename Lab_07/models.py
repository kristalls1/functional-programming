"""Предметна модель результату лабораторної роботи."""
from __future__ import annotations
from functools import total_ordering


@total_ordering
class LabResult:
    """Результат роботи; вищий бал і менша кількість спроб означають кращий результат."""
    def __init__(self, student: str, lab: int, score: float, attempts: int) -> None:
        self.student = student.strip().title()
        self.lab = int(lab)
        self.score = float(score)
        self.attempts = int(attempts)

    def _key(self) -> tuple[float, int, str]:
        return (self.score, -self.attempts, self.student.casefold())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LabResult):
            return NotImplemented
        return self._key() == other._key()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, LabResult):
            return NotImplemented
        return self._key() < other._key()

    def __repr__(self) -> str:
        return (f"LabResult(student={self.student!r}, lab={self.lab}, "
                f"score={self.score}, attempts={self.attempts})")
