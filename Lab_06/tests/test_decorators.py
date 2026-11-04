import pytest

from decorators import cached, retries, timed


def test_timed_uses_injected_clock_and_logger_and_preserves_metadata():
    ticks = iter([1.0, 1.012345])
    messages = []

    @timed("work", unit="ms", logger=messages.append, clock=lambda: next(ticks))
    def work(value: int) -> int:
        """Multiply a value."""
        return value * value

    assert work(5) == 25
    assert work.__name__ == "work"
    assert work.__doc__ == "Multiply a value."
    assert hasattr(work, "__wrapped__")
    assert any("12.345 ms" in message for message in messages)


def test_timed_logs_even_when_function_raises():
    ticks = iter([0.0, 0.01])
    messages = []

    @timed(logger=messages.append, clock=lambda: next(ticks))
    def fail():
        raise RuntimeError("broken")

    with pytest.raises(RuntimeError):
        fail()
    assert len(messages) == 1


def test_retries_succeeds_on_third_attempt_without_sleep():
    state = {"calls": 0, "sleeps": []}

    def fake_sleep(seconds):
        state["sleeps"].append(seconds)

    @retries(
        attempts=3, delay=0.1, backoff=2.0, sleep=fake_sleep,
        logger=lambda _message: None,
    )
    def flaky():
        state["calls"] += 1
        if state["calls"] < 3:
            raise TimeoutError("temporary")
        return "ok"

    assert flaky() == "ok"
    assert state["calls"] == 3
    assert state["sleeps"] == [0.1, 0.2]


def test_retries_raises_after_last_attempt():
    calls = []

    @retries(attempts=2, sleep=lambda _seconds: None)
    def always_fails():
        calls.append(1)
        raise ConnectionError("offline")

    with pytest.raises(ConnectionError):
        always_fails()
    assert len(calls) == 2


def test_retries_validates_parameters():
    with pytest.raises(ValueError):
        retries(attempts=0)
    with pytest.raises(ValueError):
        retries(delay=-1)


def test_cached_ttl_and_invalidation():
    now = {"value": 100.0}
    hits = {"count": 0}

    @cached(ttl=5.0, time_fn=lambda: now["value"])
    def price(product_id: int) -> int:
        hits["count"] += 1
        return product_id * 10

    assert price(4) == 40
    assert price(4) == 40
    assert hits["count"] == 1
    now["value"] += 6
    assert price(4) == 40
    assert hits["count"] == 2
    assert price(5) == 50
    removed = price.cache_invalidate(lambda args, _kwargs: args == (5,))
    assert removed == 1
    price.cache_clear()
    assert price(4) == 40
    assert hits["count"] == 4


def test_cached_uses_kwargs_in_key():
    calls = []

    @cached()
    def combine(*, left: int, right: int) -> int:
        calls.append(1)
        return left + right

    assert combine(left=2, right=3) == 5
    assert combine(left=2, right=3) == 5
    assert combine(left=3, right=3) == 6
    assert len(calls) == 2


def test_cached_rejects_unhashable_arguments():
    @cached()
    def count_items(items):
        return len(items)

    with pytest.raises(TypeError):
        count_items([1, 2])


def test_cached_validates_ttl():
    with pytest.raises(ValueError):
        cached(ttl=-1)


def test_decorator_metadata_preserved():
    @retries(attempts=1)
    def sample():
        """Metadata check."""
        return 1

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Metadata check."
    assert hasattr(sample, "__wrapped__")
