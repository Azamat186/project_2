import pytest

@pytest.fixture(scope="session")
def valid_card_numbers():
    return ["1234567890123456", "4567890123456789"]

@pytest.fixture(scope="session")
def invalid_card_numbers():
    return ["123456789012345", "abcde"]

@pytest.fixture(scope="session")
def valid_accounts():
    return ["123456789012", "987654321098"]

@pytest.fixture(scope="session")
def invalid_accounts():
    return ["12345678901", "abcdef"]

@pytest.fixture(scope="session")
def transactions():
    return [
        {"id": 1, "state": "done", "date": "2023-01-01"},
        {"id": 2, "state": "pending", "date": "2023-01-02"},
        {"id": 3, "state": "canceled", "date": "2023-01-03"}
    ]

@pytest.fixture(scope="session")
def iso_dates():
    return [
        ("2023-01-01T00:00:00Z", "01.01.2023"),
        ("2023-12-31T23:59:59Z", "31.12.2023"),
        ("2024-02-29T12:00:00Z", "29.02.2024"),
    ]

@pytest.fixture(scope="session")
def bad_iso_dates():
    return ["2023-13-01", "невалидная_строка"]
