"""Mutable reference implementation used only for before/after measurements."""

from dataclasses import dataclass, field


@dataclass
class MutableTask:
    id: int
    title: str
    status: str = "todo"
    priority: int = 3
    comments: list[dict[str, object]] = field(default_factory=list)
    labels: set[str] = field(default_factory=set)
    metadata: dict[str, object] = field(default_factory=dict)


def mutable_add_comment(task: MutableTask, comment: dict[str, object]) -> MutableTask:
    task.comments.append(comment)
    return task


def mutable_add_label(task: MutableTask, label: str) -> MutableTask:
    task.labels.add(label)
    return task


def mutable_change_status(task: MutableTask, status: str) -> MutableTask:
    task.status = status
    return task


def mutable_change_priority(task: MutableTask, priority: int) -> MutableTask:
    task.priority = priority
    return task
