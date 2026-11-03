"""Comparable micro-measurements for mutable and immutable update operations."""

from timeit import timeit

from baseline import MutableTask, mutable_add_label, mutable_change_priority
from core import add_label, change_priority, create_example_task


def test_measure_mutable_and_immutable_updates() -> None:
    iterations = 2000

    def mutable_operation() -> None:
        task = MutableTask(1, "Benchmark task")
        mutable_add_label(task, "backend")
        mutable_change_priority(task, 4)

    immutable_template = create_example_task()

    def immutable_operation() -> None:
        task = add_label(immutable_template, "backend")
        change_priority(task, 4)

    mutable_seconds = timeit(
        mutable_operation,
        number=iterations,
    )

    immutable_seconds = timeit(
        immutable_operation,
        number=iterations,
    )

    print(f"Mutable baseline:   " f"{mutable_seconds:.6f} s ({iterations} iterations)")

    print(
        f"Immutable model:    " f"{immutable_seconds:.6f} s ({iterations} iterations)"
    )

    print(
        "Note: this is a microbenchmark; "
        "timings depend on hardware and Python version."
    )

    assert mutable_seconds > 0
    assert immutable_seconds > 0
