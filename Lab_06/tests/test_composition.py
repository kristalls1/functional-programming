from app import build_service


def test_cache_outer_reduces_service_calls_and_retries_transient_errors():
    service, calls, logs = build_service("cache_outer")
    first = service(10)
    second = service(10)
    assert first == second == {"user_id": 10, "name": "User 10"}
    # Перший виклик містить три спроби; другий отримує результат із кешу.
    assert calls() - 1 == 3
    assert any("[retries]" in line for line in logs)
    assert any("[timed]" in line for line in logs)
    assert sum("[timed]" in line for line in logs) == 1


def test_retry_outer_retries_cached_failure_and_then_hits_cache():
    service, calls, logs = build_service("retry_outer")
    first = service(11)
    second = service(11)
    assert first == second == {"user_id": 11, "name": "User 11"}
    # Кеш знаходиться всередині retries: невдалі спроби не кешуються,
    # успішний результат кешується і повертається на наступному виклику.
    assert calls() - 1 == 3
    # The outer timer also runs on the second call, which is an inner cache hit.
    assert sum("[timed]" in line for line in logs) == 2


def test_cache_invalidation_method_available_for_cache_outer():
    service, _calls, _logs = build_service("cache_outer")
    service(12)
    assert service.cache_invalidate(lambda args, _kwargs: args == (12,)) == 1
