from core import make_processor


def get_rate(currency: str) -> float:
    rates = {
        "USD": 41.0,
        "EUR": 48.0,
        "UAH": 1.0
    }

    return rates.get(currency, 1.0)


def commission(amount: float) -> float:
    return amount * 0.98


def accept(amount: float) -> bool:
    return amount >= 50


processor = make_processor(
    get_rate=get_rate,
    commission=commission,
    accept=accept
)


transactions = [
    {
        "id": 1,
        "type": "payment",
        "amount": 100,
        "currency": "USD",
        "status": "successful"
    },
    {
        "id": 2,
        "type": "transfer",
        "amount": 30,
        "currency": "EUR",
        "status": "successful"
    },
    {
        "id": 3,
        "type": "payment",
        "amount": 200,
        "currency": "USD",
        "status": "failed"
    },
    {
        "id": 4,
        "type": "payment",
        "amount": 150,
        "currency": "EUR",
        "status": "successful"
    }
]


result = processor(transactions)


for transaction in result["transactions"]:
    print(
        "Transaction:",
        transaction["id"],
        "final amount:",
        transaction["final_amount"]
    )

print("Count:", result["count"])
print("Total:", result["total"])