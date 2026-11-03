"""Pure operations for immutable project tasks."""

from collections.abc import Iterable
from dataclasses import replace

from model import Comment, Task


def add_comment(task: Task, comment: Comment) -> Task:
    """Return a new task with one additional comment."""
    if any(existing.id == comment.id for existing in task.comments):
        raise ValueError(f"Comment with id {comment.id} already exists")
    return replace(task, comments=task.comments + (comment,))


def add_label(task: Task, label: str) -> Task:
    """Return a new task with an additional label."""
    normalized = label.strip()
    if not normalized:
        raise ValueError("Label cannot be empty")
    return replace(task, labels=task.labels | frozenset({normalized}))


def change_status(task: Task, status: str) -> Task:
    """Return a new task with an updated status."""
    allowed = {"todo", "in_progress", "done", "blocked"}
    if status not in allowed:
        raise ValueError(f"Status must be one of: {', '.join(sorted(allowed))}")
    return replace(task, status=status)


def change_priority(task: Task, priority: int) -> Task:
    """Return a new task with an updated priority."""
    if not 1 <= priority <= 5:
        raise ValueError("Priority must be between 1 and 5")
    return replace(task, priority=priority)


def add_comments(task: Task, comments: Iterable[Comment]) -> Task:
    """Return a new task with multiple comments, without mutating the original."""
    result = task
    for comment in comments:
        result = add_comment(result, comment)
    return result


def task_summary(task: Task) -> str:
    """Build a short human-readable task summary."""
    return (
        f"#{task.id} {task.title} | status={task.status} | "
        f"priority={task.priority} | comments={len(task.comments)}"
    )


def create_example_task() -> Task:
    """Create a deterministic example used by tests and the demo."""
    return Task(
        id=1,
        title="Prepare project documentation",
        description="Write and review the project documentation.",
        status="todo",
        priority=3,
        comments=(),
        labels=frozenset({"documentation", "university"}),
        metadata={"author": "Khrystyna", "department": "Computer Science"},
    )
