"""Демонстрація композиції декораторів для сервісної функції."""
from __future__ import annotations

from closures import make_counter, make_logger
from decorators import cached, retries, timed


def build_service(order: str = "cache_outer"):
    """Створює сервіс із заданим порядком декораторів і спільним станом."""
    logs: list[str] = []
    logger = make_logger("SERVICE", logs.append)
    calls = make_counter()
    attempts_by_user: dict[int, int] = {}

    def unstable_fetch(user_id: int) -> dict[str, object]:
        calls()
        attempts_by_user[user_id] = attempts_by_user.get(user_id, 0) + 1
        if attempts_by_user[user_id] < 3:
            raise TimeoutError(f"тимчасова помилка для користувача {user_id}")
        return {"user_id": user_id, "name": f"User {user_id}"}

    retry_layer = retries(
        attempts=3, delay=0.1, backoff=2.0, jitter=0.0,
        sleep=lambda _seconds: None, logger=logger,
    )(unstable_fetch)
    timed_retry = timed(
        "service", unit="ms", logger=logger, clock=_fake_clock()
    )(retry_layer)

    if order == "cache_outer":
        service = cached(ttl=30.0)(timed_retry)
    elif order == "retry_outer":
        service = timed(
            "service", unit="ms", logger=logger, clock=_fake_clock()
        )(retries(
            attempts=3, delay=0.1, backoff=2.0, sleep=lambda _seconds: None,
            logger=logger,
        )(cached(ttl=30.0)(unstable_fetch)))
    else:
        raise ValueError("order має бути 'cache_outer' або 'retry_outer'.")

    return service, calls, logs


def _fake_clock():
    """Повертає годинник із детермінованим кроком для демонстраційного логу."""
    ticks = iter(i * 0.001 for i in range(1000))
    return lambda: next(ticks)


def main() -> None:
    print("=== Лабораторна робота 6 — варіант 15 ===")
    for order in ("cache_outer", "retry_outer"):
        service, calls, logs = build_service(order)
        print(f"\nПорядок: {order}")
        print("Перший виклик:", service(7))
        print("Повторний виклик:", service(7))
        print("Кількість звернень до сервісної функції:", calls() - 1)
        print("Лог:")
        for line in logs:
            print(" ", line)
        print("Очищення кешу та повторний виклик:")
        clear = getattr(service, "cache_clear", None)
        if clear is not None:
            clear()
        print(service(7))


if __name__ == "__main__":
    main()
