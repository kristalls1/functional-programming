"""Параметризовані декоратори таймінгу, повторів і кешування."""
from __future__ import annotations

import functools
import random
import threading
import time
from collections.abc import Callable
from typing import Any, Hashable, Literal, ParamSpec, Protocol, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")
R_co = TypeVar("R_co", covariant=True)


class CachedFunction(Protocol[P, R_co]):
    """Callable returned by ``cached``, including its cache controls."""

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co: ...

    def cache_clear(self) -> None: ...

    def cache_invalidate(
        self, predicate: Callable[[tuple[Any, ...], dict[str, Any]], bool]
    ) -> int: ...


def timed(
    label: str | None = None,
    *,
    unit: Literal["s", "ms", "us"] = "ms",
    logger: Callable[[str], None] = print,
    clock: Callable[[], float] = time.perf_counter,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Фабрика декоратора, що вимірює час виконання функції."""
    if unit not in ("s", "ms", "us"):
        raise ValueError("unit має бути 's', 'ms' або 'us'.")
    factor = {"s": 1.0, "ms": 1e3, "us": 1e6}[unit]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        name = label or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            started = clock()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = (clock() - started) * factor
                logger(f"[timed] {name} took {elapsed:.3f} {unit}")
        return wrapper
    return decorator


def retries(
    attempts: int = 3,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    delay: float = 0.0,
    backoff: float = 1.0,
    jitter: float = 0.0,
    *,
    sleep: Callable[[float], None] = time.sleep,
    logger: Callable[[str], None] = lambda _message: None,
    random_fn: Callable[[], float] = random.random,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Повторює виклик після заданих винятків із backoff та jitter."""
    if attempts < 1:
        raise ValueError("attempts має бути не менше 1.")
    if delay < 0 or jitter < 0 or backoff < 1:
        raise ValueError("delay і jitter мають бути >= 0, backoff — >= 1.")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: BaseException | None = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    last_error = error
                    if attempt == attempts:
                        logger(f"[retries] failed after {attempt} attempts: {error!r}")
                        break
                    wait = delay * (backoff ** (attempt - 1))
                    if jitter:
                        wait += random_fn() * jitter
                    logger(f"[retries] attempt {attempt} failed; wait {wait:.3f}s")
                    sleep(wait)
            assert last_error is not None
            raise last_error
        return wrapper
    return decorator


def make_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Hashable:
    """Формує ключ кешу; аргументи мають бути хешованими."""
    try:
        key = (args, tuple(sorted(kwargs.items())))
        hash(key)
        return key
    except TypeError as error:
        raise TypeError("Аргументи функції мають бути хешованими.") from error


def cached(
    *,
    ttl: float | None = None,
    time_fn: Callable[[], float] = time.time,
) -> Callable[[Callable[P, R]], CachedFunction[P, R]]:
    """Кешує результати з необов'язковим TTL та інвалідацією записів."""
    if ttl is not None and ttl < 0:
        raise ValueError("ttl не може бути від'ємним.")

    def decorator(func: Callable[P, R]) -> CachedFunction[P, R]:
        cache: dict[Hashable, tuple[float | None, R]] = {}
        # Lock the computation too, so simultaneous misses share one result.
        lock = threading.RLock()

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(args, kwargs)
            with lock:
                now = time_fn()
                entry = cache.get(key)
                if entry is not None:
                    expires_at, value = entry
                    if expires_at is None or now < expires_at:
                        return value
                    del cache[key]
                value = func(*args, **kwargs)
                expires_at = None if ttl is None else time_fn() + ttl
                cache[key] = (expires_at, value)
                return value

        def cache_clear() -> None:
            with lock:
                cache.clear()

        def cache_invalidate(
            predicate: Callable[[tuple[Any, ...], dict[str, Any]], bool]
        ) -> int:
            removed = 0
            with lock:
                for key in list(cache):
                    args_key, kwargs_key = key
                    if predicate(args_key, dict(kwargs_key)):
                        del cache[key]
                        removed += 1
            return removed

        setattr(wrapper, "cache_clear", cache_clear)
        setattr(wrapper, "cache_invalidate", cache_invalidate)
        return cast(CachedFunction[P, R], wrapper)
    return decorator
