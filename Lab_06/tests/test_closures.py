from closures import make_counter, make_logger


def test_counter_keeps_state():
    counter = make_counter(4)
    assert counter() == 5
    assert counter() == 6


def test_logger_closes_over_prefix():
    messages = []
    logger = make_logger("TEST", messages.append)
    logger("ready")
    assert messages == ["[TEST] ready"]
