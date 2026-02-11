import pytest
from src.generators import *

@pytest.fixture(scope="module")
def sample_transactions():
    """Генерация фиксированных транзакций."""
    return [
        {"id": 1, "description": "Описание первой транзакции", "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "description": "Вторая транзакция", "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "description": "Третья транзакция", "operationAmount": {"currency": {"code": "USD"}}}
    ]

@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        ([{"description": "Операция 1"}], ["Операция 1"]),
        ([{"description": ""}], [""]),  # Пустой description
        ([{"description": "Op 1"}, {"description": "Op 2"}], ["Op 1", "Op 2"]),  # Много записей
        ([], [])  # Пустой список
    ],
    ids=[
        "single_description",
        "empty_description",
        "many_descriptions",
        "no_transactions"
    ]
)
def test_transaction_descriptions(transactions, expected_descriptions):
    descriptions = transaction_descriptions(transactions)
    actual_descriptions = list(descriptions)
    assert actual_descriptions == expected_descriptions


# Параметризированные тесты для filter_by_currency
@pytest.mark.parametrize(
    "input_data, expected_ids",
    [

        ([{"id": 1, "operationAmount": {"currency": {"code": "USD"}}}], [1]),


        ([], []),


        ([{"id": 1, "operationAmount": {"currency": {"code": "RUB"}}}], []),


        ([{"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
          {"id": 2, "operationAmount": {"currency": {"code": "USD"}}}], [2]),


        ([{"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
          {"id": 2, "operationAmount": {"currency": {"code": "USD"}}}], [1, 2]),


        ([{"id": 1, "operationAmount": {}}], []),
    ],
    ids=[
        "simple_case",
        "empty_list",
        "no_match",
        "partial_match",
        "all_match",
        "missing_key"
    ]
)
def test_filter_by_currency(input_data, expected_ids):
    result = list(filter_by_currency(input_data, "USD"))
    result_ids = [item["id"] for item in result]
    assert sorted(result_ids) == sorted(expected_ids)

# Тест для transaction_descriptions
def test_transaction_descriptions(sample_transactions):
    descriptions = transaction_descriptions(sample_transactions)
    actual_results = list(descriptions)
    assert all(isinstance(d, str) for d in actual_results)

# Параметризованные тесты для card_numbers_generator
@pytest.mark.parametrize(
    "start, stop, expected_first, expected_last",
    [
        (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (1000, 1002, "0000 0000 0000 1000", "0000 0000 0000 1002"),  # Среднее число
        (9999999999999995, 9999999999999999, "9999 9999 9999 9995", "9999 9999 9999 9999")  # Максимальные границы
    ],
    ids=[
        "small_range",
        "medium_range",
        "maximal_range"
    ]
)
def test_card_number_generator(start, stop, expected_first, expected_last):
    gen = card_number_generator(start, stop)
    numbers = list(gen)
    first_number = numbers[0]
    last_number = numbers[-1]
    assert first_number == expected_first and last_number == expected_last
