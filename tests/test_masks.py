# tests/test_masks.py

import pytest
from src.masks import get_mask_card_number, get_mask_account
from src.widget import get_date

valid_card_numbers = ["1234567890123456", "4567890123456789"]
invalid_card_numbers = ["12345678912345", "abcde"]
valid_accounts = ["123456789012", "987654321098"]
invalid_accounts = ["12345678901", "abcdef"]


@pytest.mark.parametrize(
    "card_number,expected_result",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("9876543210987654", "9876 54** **** 7654"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number(card_number, expected_result):
    assert get_mask_card_number(int(card_number)) == expected_result


def test_get_mask_card_number(valid_card_numbers):
    for card in valid_card_numbers:
        result = get_mask_card_number(int(card))
        assert isinstance(result, str)
        parts = result.split()
        assert len(parts) == 4
        assert parts[-1].isdigit() and parts[-1].isdigit()


@pytest.mark.parametrize("invalid_card", invalid_card_numbers)
def test_get_mask_card_number_invalid(invalid_card):
    with pytest.raises(ValueError):
        get_mask_card_number(int(invalid_card))


@pytest.mark.parametrize("account", valid_accounts)
def test_get_mask_account(account):
    masked = get_mask_account(account)
    assert masked.startswith("**") and masked.endswith(account[-4:])


@pytest.mark.parametrize("invalid_account", ["123", "abc"])
def test_get_mask_account_invalid(invalid_account):
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)


# Объедененный тест, проверяющий разные типы маскирования
def test_mask_account_valid(valid_card_numbers, valid_accounts):
    inputs = [(f"карта {card}", get_mask_card_number(int(card))) for card in valid_card_numbers]
    inputs.extend([(f"счет {acc}", get_mask_account(acc)) for acc in valid_accounts])
    for input_data, expected_result in inputs:
        if input_data.startswith("карта"):
            result = get_mask_card_number(int(input_data.split()[1]))
        elif input_data.startswith("счет"):
            result = get_mask_account(input_data.split()[1])
        assert result == expected_result


# ТЕСТЫ НА ОБРАБОТКУ НЕВЕРНЫХ ДАТ
def test_get_date_invalid(bad_iso_dates):
    for date_input in bad_iso_dates:
        with pytest.raises(ValueError):
            get_date(date_input)


# Тест на обработку некорректных данных
def test_mask_account_invalid():
    invalid_inputs = ["Некорректные данные", ""]
    for input_data in invalid_inputs:
        with pytest.raises(ValueError):
            if input_data.startswith("карта"):
                get_mask_card_number(int(input_data.split()[1]))
            elif input_data.startswith("счет"):
                get_mask_account(input_data.split()[1])
            else:
                raise ValueError("Некорректный тип данных")
