# tests/test_processing.py

from src.processings import sort_by_date, datetime


def transactions():
    return [
        {"id": 1, "state": "done", "date": "2023-01-01"},
        {"id": 2, "state": "pending", "date": "2023-01-02"},
        {"id": 3, "state": "canceled", "date": "2023-01-03"},
    ]


def filter_by_state(transactions, state):
    filtered_transactions = []
    for transaction in transactions:
        if transaction["state"] == state:
            filtered_transactions.append(transaction)
    return filtered_transactions


def sort_by_date(transactions, reverse=False):
    sorted_transactions = sorted(transactions, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=reverse)
    return sorted_transactions


def test_filter_by_state(transactions):
    done_txns = filter_by_state(transactions, "done")
    assert len(done_txns) == 1
    assert done_txns[0]["id"] == 1

    pending_txns = filter_by_state(transactions, "pending")
    assert len(pending_txns) == 1
    assert pending_txns[0]["id"] == 2

    canceled_txns = filter_by_state(transactions, "canceled")
    assert len(canceled_txns) == 1
    assert canceled_txns[0]["id"] == 3


def test_sort_by_date(transactions):
    ascending_sorted = sort_by_date(transactions)
    descending_sorted = sort_by_date(transactions, reverse=True)

    assert ascending_sorted[0]["id"] == 1
    assert descending_sorted[0]["id"] == 3
