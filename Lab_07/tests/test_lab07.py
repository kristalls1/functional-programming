from __future__ import annotations
import io
import json
from pathlib import Path
import pytest
from operator import attrgetter, itemgetter, methodcaller
from loaders import load_results
from models import LabResult
from pipeline import clean_and_rank, pipeline, final_score, normalize_result

SAMPLE = [
    {"student": " alice ", "lab": "1", "score": "90", "attempts": "1", "submitted": "true"},
    {"student": "bob", "lab": "1", "score": "95", "attempts": "2", "submitted": "true"},
    {"student": "carol", "lab": "1", "score": "100", "attempts": "1", "submitted": "false"},
]


def test_pipeline_uses_functions_in_order():
    assert pipeline(3, lambda x: x + 1, lambda x: x * 2, lambda x: x + 1) == 9


def test_partial_configured_final_score():
    from functools import partial
    score_with_penalty = partial(final_score, penalty=1.0)
    row = normalize_result(SAMPLE[1])
    assert score_with_penalty(row)["final_score"] == 94.0


def test_load_json_string():
    assert load_results(json.dumps(SAMPLE)) == SAMPLE


def test_load_list_copies_records():
    loaded = load_results(SAMPLE)
    assert loaded == SAMPLE and loaded[0] is not SAMPLE[0]


def test_load_json_path(tmp_path: Path):
    path = tmp_path / "data.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    assert load_results(path) == SAMPLE
    assert load_results(str(path)) == SAMPLE


def test_load_csv_path(tmp_path: Path):
    path = tmp_path / "data.csv"
    path.write_text("student,lab,score,attempts,submitted\nalice,1,90,1,true\n", encoding="utf-8")
    assert load_results(path)[0]["student"] == "alice"


def test_load_open_json_file():
    stream = io.StringIO(json.dumps(SAMPLE))
    assert load_results(stream) == SAMPLE


def test_load_open_csv_file():
    stream = io.StringIO("student,lab,score,attempts,submitted\nalice,1,90,1,true\n")
    stream.name = "data.csv"
    assert load_results(stream)[0]["score"] == "90"


def test_unsupported_type():
    with pytest.raises(TypeError):
        load_results(42)


def test_normalize_and_score():
    normalized = normalize_result(SAMPLE[0])
    assert normalized["student"] == "Alice" and normalized["lab"] == 1
    assert final_score(normalized)["final_score"] == 90.0


def test_clean_and_rank_filters_and_sorts():
    ranked = clean_and_rank(SAMPLE, top=2)
    assert [row["student"] for row in ranked] == ["Bob", "Alice"]
    assert ranked[0]["final_score"] == 94.5


def test_top_zero_and_negative():
    assert clean_and_rank(SAMPLE, top=0) == []
    with pytest.raises(ValueError):
        clean_and_rank(SAMPLE, top=-1)


def test_validation_errors():
    with pytest.raises(ValueError):
        normalize_result({"student": "A", "lab": 1, "score": 101, "attempts": 1, "submitted": True})
    with pytest.raises(ValueError):
        load_results([1, 2])


def test_total_ordering_all_comparisons():
    best = LabResult("Bob", 1, 95, 1)
    middle = LabResult("Alice", 1, 95, 2)
    low = LabResult("Carol", 1, 80, 1)
    assert best > middle and best >= middle
    assert middle < best and middle <= best
    assert best != middle and best == LabResult(" bob ", 1, 95, 1)
    assert sorted([low, middle, best]) == [low, middle, best]


def test_total_ordering_other_type_returns_not_implemented():
    result = LabResult("A", 1, 90, 1)
    assert result.__eq__(object()) is NotImplemented
    assert result.__lt__(object()) is NotImplemented


def test_operator_helpers():
    rows = [{"student": " Alice ", "score": 90}, {"student": "Bob", "score": 95}]
    assert sorted(rows, key=itemgetter("score"), reverse=True)[0]["student"] == "Bob"
    assert methodcaller("title")(methodcaller("strip")("  alice  ")) == "Alice"
    objects = [LabResult("Alice", 1, 90, 1), LabResult("Bob", 1, 95, 1)]
    assert attrgetter("score")(max(objects)) == 95
