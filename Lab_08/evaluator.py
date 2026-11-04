from __future__ import annotations
from typing import assert_never
from model import And, Eq, Not, Or, Query, SupportsRecordLookup
class QueryEvaluationError(ValueError):
    """Raised when a query refers to an absent record field."""
def eval_query(query: Query, record: SupportsRecordLookup) -> bool:
    match query:
        case Eq(field=field, value=value, operator="=="):
            try:
                actual = record[field.name]
            except KeyError as exc:
                raise QueryEvaluationError(f"record does not contain field: {field.name}") from exc
            return actual == value
        case And(left=left, right=right):
            return eval_query(left, record) and eval_query(right, record)
        case Or(left=left, right=right):
            return eval_query(left, record) or eval_query(right, record)
        case Not(query=inner):
            return not eval_query(inner, record)
    assert_never(query)
