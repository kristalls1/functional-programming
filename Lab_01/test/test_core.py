from copy import deepcopy

from core import make_processor


def test_referential_transparency():
    transactions = [
        {
            "id": 1,
            "type": "payment",
            "amount": 100,
            "currency": "USD",
            "status": "successful"
        }
    ]

    processor = make_processor(
        get_rate=lambda currency: 40.0,
        commission=lambda amount: amount * 0.9,
        accept=lambda amount: amount >= 50
    )

    result1 = processor(transactions)
    result2 = processor(transactions)

    assert result1 == result2


def test_no_mutation():
    transactions = [
        {
            "id": 1,
            "type": "payment",
            "amount": 100,
            "currency": "USD",
            "status": "successful"
        }
    ]

    original = deepcopy(transactions)

    processor = make_processor(
        get_rate=lambda currency: 40.0,
        commission=lambda amount: amount * 0.9,
        accept=lambda amount: amount >= 50
    )

    processor(transactions)

    assert transactions == original


def test_callable_policies():
    transactions = [
        {
            "id": 1,
            "type": "payment",
            "amount": 100,
            "currency": "USD",
            "status": "successful"
        }
    ]

    processor = make_processor(
        get_rate=lambda currency: 40.0,
        commission=lambda amount: amount * 0.9,
        accept=lambda amount: amount >= 50
    )

    result = processor(transactions)

    assert result["count"] == 1
    assert result["total"] == 3600.0