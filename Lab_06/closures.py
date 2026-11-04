"""Замикання для логування та підрахунку викликів."""
from collections.abc import Callable


def make_logger(
    prefix: str, sink: Callable[[str], None] = print
) -> Callable[[str], None]:
    """Створює логер, який зберігає префікс у замиканні."""
    def log(message: str) -> None:
        sink(f"[{prefix}] {message}")
    return log


def make_counter(start: int = 0) -> Callable[[], int]:
    """Створює лічильник зі змінним станом, який зберігається в closure."""
    value = start

    def increment() -> int:
        nonlocal value
        value += 1
        return value

    return increment
