from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias, Union
Scalar: TypeAlias = str | int | float | bool | None
ComparisonOperator: TypeAlias = Literal["=="]
LogicalOperator: TypeAlias = Literal["and", "or", "not"]
Operator: TypeAlias = Union[ComparisonOperator, LogicalOperator]
class SupportsRecordLookup(Protocol):
    def __getitem__(self, key: str) -> object: ...
@dataclass(frozen=True)
class Field:
    name: str
@dataclass(frozen=True)
class Eq:
    field: Field
    value: Scalar
    operator: ComparisonOperator = "=="
@dataclass(frozen=True)
class And:
    left: Query
    right: Query
@dataclass(frozen=True)
class Or:
    left: Query
    right: Query
@dataclass(frozen=True)
class Not:
    query: Query
Query: TypeAlias = Union[Eq, And, Or, Not]
