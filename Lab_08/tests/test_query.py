import pytest
from evaluator import QueryEvaluationError, eval_query
from model import And, Eq, Field, Not, Or
from pretty import render_query
def test_eq() -> None:
    assert eval_query(Eq(Field("city"), "Lviv"), {"city":"Lviv"})
    assert not eval_query(Eq(Field("city"), "Lviv"), {"city":"Kyiv"})
def test_and() -> None:
    q=And(Eq(Field("age"),20),Eq(Field("active"),True))
    assert eval_query(q,{"age":20,"active":True})
    assert not eval_query(q,{"age":20,"active":False})
def test_or() -> None:
    q=Or(Eq(Field("city"),"Lviv"),Eq(Field("city"),"Kyiv"))
    assert eval_query(q,{"city":"Kyiv"})
    assert not eval_query(q,{"city":"Odesa"})
def test_not() -> None:
    assert eval_query(Not(Eq(Field("active"),False)),{"active":True})
    assert not eval_query(Not(Eq(Field("active"),False)),{"active":False})
def test_nested_query() -> None:
    q=And(Eq(Field("city"),"Lviv"),Or(Eq(Field("age"),20),Not(Eq(Field("active"),False))))
    assert eval_query(q,{"city":"Lviv","age":18,"active":True})
    assert not eval_query(q,{"city":"Kyiv","age":20,"active":True})
def test_missing_field() -> None:
    with pytest.raises(QueryEvaluationError,match="does not contain field"):
        eval_query(Eq(Field("email"),"x"),{"name":"Anna"})
def test_render() -> None:
    q=And(Eq(Field("city"),"Lviv"),Not(Eq(Field("active"),False)))
    assert render_query(q)=="(city == 'Lviv' AND (NOT active == False))"
def test_immutable() -> None:
    q=Eq(Field("age"),18)
    with pytest.raises(Exception):
        q.value=21  # type: ignore[misc]
def test_record_not_modified() -> None:
    row={"city":"Lviv","age":20}; before=row.copy()
    eval_query(And(Eq(Field("city"),"Lviv"),Eq(Field("age"),20)),row)
    assert row==before
def test_short_circuit_and() -> None:
    assert not eval_query(And(Eq(Field("active"),True),Eq(Field("missing"),1)),{"active":False})
def test_short_circuit_or() -> None:
    assert eval_query(Or(Eq(Field("active"),True),Eq(Field("missing"),1)),{"active":True})
def test_empty_key() -> None:
    assert eval_query(Eq(Field(""),1),{"":1})
