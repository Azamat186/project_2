import os
from unittest.mock import MagicMock, patch
from pathlib import Path
from typing import List, Dict
import pytest
import pandas as pd  # Не забудьте добавить импорт pandas
from src.data_readers import read_csv_transactions, read_excel_transactions


@pytest.fixture(scope="session")
def csv_file():
    """Возвращает временный CSV файл"""
    content = b"id,date,amount\n1,2023-01-01,100"
    with open("test_transactions.csv", "wb") as f:
        f.write(content)
    yield "test_transactions.csv"
    os.remove("test_transactions.csv")


@pytest.fixture(scope="session")
def excel_file():
    """Возвращает временный Excel файл"""
    from io import BytesIO
    output = BytesIO()
    df = pd.DataFrame({"id": [1], "date": ["2023-01-01"], "amount": [100]})
    df.to_excel(output, index=False)
    output.seek(0)
    with open("test_transactions.xlsx", "wb") as f:
        f.write(output.getvalue())
    yield "test_transactions.xlsx"
    os.remove("test_transactions.xlsx")


@patch("pandas.read_csv")
def test_read_csv_transactions(mock_pandas):
    mock_df = MagicMock(spec=pd.DataFrame)
    mock_df.to_dict.return_value = [{"id": 1, "date": "2023-01-01", "amount": 100}]
    mock_pandas.return_value = mock_df
    result = read_csv_transactions("some/path/to/file.csv")
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["id"] == 1


@patch("pandas.read_excel")
def test_read_excel_transactions(mock_pandas):
    mock_df = MagicMock(spec=pd.DataFrame)
    mock_df.to_dict.return_value = [{"id": 1, "date": "2023-01-01", "amount": 100}]
    mock_pandas.return_value = mock_df
    result = read_excel_transactions("some/path/to/file.xlsx")
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["id"] == 1
