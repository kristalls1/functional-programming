from typing import Callable, TypedDict


class Transaction(TypedDict):
    id: int
    type: str
    amount: float
    currency: str
    status: str


class ProcessedTransaction(TypedDict):
    id: int
    type: str
    amount: float
    currency: str
    status: str
    converted_amount: float
    final_amount: float


RateFn = Callable[[str], float]
CommissionFn = Callable[[float], float]
FilterFn = Callable[[float], bool]


def is_successful(transaction: Transaction) -> bool:
    return transaction["status"] == "successful"


def convert_amount(
    amount: float,
    currency: str,
    get_rate: RateFn
) -> float:
    return amount * get_rate(currency)


def apply_commission(
    amount: float,
    commission: CommissionFn
) -> float:
    return commission(amount)


def with_processed_amount(
    transaction: Transaction,
    converted_amount: float,
    final_amount: float
) -> ProcessedTransaction:
    return {
        **transaction,
        "converted_amount": converted_amount,
        "final_amount": final_amount
    }


def make_processor(
    *,
    get_rate: RateFn,
    commission: CommissionFn,
    accept: FilterFn
) -> Callable[[list[Transaction]], dict[str, object]]:

    def process(
        transactions: list[Transaction]
    ) -> dict[str, object]:

        processed = []
        total = 0.0

        for transaction in transactions:

            if not is_successful(transaction):
                continue

            amount = transaction["amount"]

            if not accept(amount):
                continue

            converted_amount = convert_amount(
                amount,
                transaction["currency"],
                get_rate
            )

            final_amount = apply_commission(
                converted_amount,
                commission
            )

            new_transaction = with_processed_amount(
                transaction,
                converted_amount,
                final_amount
            )

            processed.append(new_transaction)
            total += final_amount

        return {
            "count": len(processed),
            "total": total,
            "transactions": processed
        }

    return process