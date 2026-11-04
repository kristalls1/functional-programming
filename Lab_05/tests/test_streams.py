from itertools import count, islice
import pytest

from streams import (
    after_threshold, below_threshold, bounded_measurements, drop, moving_average,
    prefix_statistics, prefix_sums, sliding_window, take, valid_measurements,
)


class Provider:
    def __init__(self, values, sentinel=None):
        self.values = iter(values)
        self.sentinel = sentinel
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return next(self.values, self.sentinel)


def test_callable_provider_and_filtering():
    provider = Provider([20, 999, 21, -100, 22])
    assert list(bounded_measurements(provider)) == [20.0, 21.0, 22.0]


def test_sentinel_stops_stream():
    provider = Provider([1, 2], sentinel=None)
    assert list(bounded_measurements(provider)) == [1.0, 2.0]


def test_lazy_provider_only_called_when_requested():
    provider = Provider([10, 11, 12, 13, 14])
    stream = bounded_measurements(provider)
    assert take(2, stream) == [10.0, 11.0]
    assert provider.calls == 2


def test_take_drop_with_infinite_count():
    values = count(1)
    assert take(4, values) == [1, 2, 3, 4]
    assert take(3, values) == [5, 6, 7]
    assert list(islice(drop(10, count(0)), 3)) == [10, 11, 12]


def test_take_drop_zero_and_negative():
    assert take(0, [1, 2]) == []
    assert list(drop(0, [1, 2])) == [1, 2]
    with pytest.raises(ValueError):
        take(-1, [])
    with pytest.raises(ValueError):
        drop(-1, [])


def test_sliding_window_and_short_source():
    assert list(sliding_window([1, 2, 3, 4], 3)) == [(1, 2, 3), (2, 3, 4)]
    assert list(sliding_window([1, 2], 3)) == []
    assert list(sliding_window([], 2)) == []


def test_invalid_window_size():
    with pytest.raises(ValueError):
        list(sliding_window([1], 0))


def test_moving_average():
    assert list(moving_average([10, 20, 30, 40], 2)) == [15, 25, 35]


def test_prefix_accumulation_and_statistics():
    assert list(prefix_sums([1, 2, 3, 4])) == [1, 3, 6, 10]
    assert list(prefix_statistics([10, 20, 30])) == [
        (1, 10.0, 10.0), (2, 30.0, 15.0), (3, 60.0, 20.0)
    ]


def test_threshold_iterators():
    assert list(below_threshold([1, 2, 3, 1], 2)) == [1, 2]
    assert list(after_threshold([1, 2, 3, 4], 2)) == [3, 4]


def test_invalid_filter_bounds():
    with pytest.raises(ValueError):
        list(valid_measurements([1], 10, 0))
