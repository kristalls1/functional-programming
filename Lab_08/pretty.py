from __future__ import annotations
from typing import assert_never
from model import And, Eq, Not, Or, Query
def render_query(query: Query) -> str:
    match query:
        case Eq(field=field, value=value, operator="=="):
            return f"{field.name} == {value!r}"
        case And(left=left, right=right):
            return f"({render_query(left)} AND {render_query(right)})"
        case Or(left=left, right=right):
            return f"({render_query(left)} OR {render_query(right)})"
        case Not(query=inner):
            return f"(NOT {render_query(inner)})"
    assert_never(query)
