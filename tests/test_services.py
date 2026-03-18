from unittest.mock import patch

import pytest

from src.services import investment_bank


@pytest.fixture
def sample_transactions():
    return [
        {'Date operation': '2023-05-01', 'Amount operation': 1712},
        {'Date operation': '2023-05-15', 'Amount operation': 2345},
        {'Date operation': '2023-06-01', 'Amount operation': 500},
    ]


@patch('src.services.logging.error')
def test_valid_case(mock_log_error, sample_transactions):
    result = investment_bank('2023-05', sample_transactions, 50)
    assert result == 43.0


@patch('src.services.logging.error')
def test_invalid_limit(mock_log_error, sample_transactions):
    with pytest.raises(ValueError):
        investment_bank('2023-05', sample_transactions, 15)


@patch('src.services.logging.error')
def test_empty_transactions(mock_log_error):
    result = investment_bank('2023-05', [], 50)
    assert result == 0.0
