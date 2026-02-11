# tests/test_widget.py
import pytest
from src.widget import get_date

def test_get_date_valid(iso_dates):
    for date_input, expected_output in iso_dates:
        result = get_date(date_input)
        assert result == expected_output

def test_get_date_invalid(bad_iso_dates):
    for date_input in bad_iso_dates:
        with pytest.raises(ValueError):
            get_date(date_input)
