from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from core import (
    add_comment,
    add_label,
    change_priority,
    change_status,
    create_example_task,
)
from model import Comment, Task, make_metadata


def sample_comment(comment_id: int = 1) -> Comment:
    return Comment(
        comment_id,
        "Anna",
        "Started working on this task.",
        "2026-11-03",
    )


def test_domain_entities_are_frozen() -> None:
    task = create_example_task()

    with pytest.raises(FrozenInstanceError):
        task.status = "done"  # type: ignore[misc]

    comment = sample_comment()

    with pytest.raises(FrozenInstanceError):
        comment.text = "Changed"  # type: ignore[misc]


def test_collections_use_immutable_types() -> None:
    task = create_example_task()

    assert isinstance(task.comments, tuple)
    assert isinstance(task.labels, frozenset)
    assert isinstance(task.metadata, MappingProxyType)


def test_add_comment_returns_new_task_and_preserves_original() -> None:
    task = create_example_task()
    original_comments = task.comments

    updated = add_comment(task, sample_comment())

    assert updated is not task
    assert task.comments is original_comments
    assert task.comments == ()
    assert len(updated.comments) == 1
    assert updated.comments[0].text == "Started working on this task."


def test_add_label_returns_new_task_and_preserves_original() -> None:
    task = create_example_task()

    updated = add_label(task, "urgent")

    assert updated is not task
    assert "urgent" not in task.labels
    assert "urgent" in updated.labels


def test_change_status_returns_new_task() -> None:
    task = create_example_task()

    updated = change_status(task, "in_progress")

    assert updated is not task
    assert task.status == "todo"
    assert updated.status == "in_progress"


def test_change_priority_returns_new_task() -> None:
    task = create_example_task()

    updated = change_priority(task, 5)

    assert updated is not task
    assert task.priority == 3
    assert updated.priority == 5


def test_metadata_is_read_only_and_copied() -> None:
    source = {"owner": "Anna"}
    metadata = make_metadata(source)

    source["owner"] = "Changed"

    assert metadata["owner"] == "Anna"

    with pytest.raises(TypeError):
        metadata["owner"] = "Blocked"  # type: ignore[index]


def test_task_constructor_defensively_copies_collections() -> None:
    labels: set[str] = {"frontend"}
    comments: list[Comment] = []
    metadata: dict[str, object] = {"team": "A"}

    task = Task(
        10,
        "Test",
        "Description",
        "todo",
        2,
        comments,  # type: ignore[arg-type]
        labels,  # type: ignore[arg-type]
        metadata,
    )

    labels.add("backend")
    comments.append(sample_comment())
    metadata["team"] = "B"

    assert task.labels == frozenset({"frontend"})
    assert task.comments == ()
    assert task.metadata["team"] == "A"


def test_duplicate_comment_id_is_rejected() -> None:
    task = add_comment(create_example_task(), sample_comment())

    with pytest.raises(ValueError, match="already exists"):
        add_comment(task, sample_comment())


def test_invalid_status_and_priority_are_rejected() -> None:
    with pytest.raises(ValueError):
        change_status(create_example_task(), "unknown")

    with pytest.raises(ValueError):
        change_priority(create_example_task(), 6)


def test_task_is_hashable() -> None:
    task = create_example_task()
    updated = add_label(task, "backend")

    tasks = {task, updated}

    assert len(tasks) == 2
    assert {task: "original", updated: "updated"}[task] == "original"
