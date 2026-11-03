"""Immutable domain models for project task management (variant 15)."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


def make_metadata(
    source: Mapping[str, object] | None = None, **kwargs: object
) -> Mapping[str, object]:
    """Create a read-only metadata mapping backed by a private copy."""
    data: dict[str, object] = dict(source or {})
    data.update(kwargs)
    return MappingProxyType(data)


@dataclass(frozen=True, slots=True)
class Comment:
    """A comment attached to a project task."""

    id: int
    author: str
    text: str
    created_at: str


@dataclass(frozen=True, slots=True)
class Task:
    """Immutable project task."""

    id: int
    title: str
    description: str
    status: str
    priority: int
    comments: tuple[Comment, ...]
    labels: frozenset[str]
    metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("Task id must be positive")
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 and 5")
        if self.status not in {"todo", "in_progress", "done", "blocked"}:
            raise ValueError("Unsupported task status")
        object.__setattr__(self, "comments", tuple(self.comments))
        object.__setattr__(self, "labels", frozenset(self.labels))
        object.__setattr__(self, "metadata", make_metadata(self.metadata))

    def __hash__(self) -> int:
        """Hash the immutable domain fields; metadata is intentionally excluded.

        MappingProxyType is read-only but not hashable. Excluding metadata is safe:
        equal Task objects still have identical values for every field used here.
        """
        return hash(
            (
                self.id,
                self.title,
                self.description,
                self.status,
                self.priority,
                self.comments,
                self.labels,
            )
        )
