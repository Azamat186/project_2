from unittest.mock import patch, MagicMock
from src.utils import read_json_file
import json

@patch('builtins.open', create=True)
def test_read_valid_json(mock_open):
    """Тест успешного прочтения JSON-файла"""
    mock_open.return_value.__enter__.return_value.read.return_value = '[{"id": 1}, {"id": 2}]'
    result = read_json_file('some/path/to/file.json')
    assert isinstance(result, list)
    assert len(result) > 0

@patch('builtins.open', side_effect=FileNotFoundError())
def test_read_nonexistent_file(mock_open):
    """Тест обработки ситуации отсутствия файла"""
    result = read_json_file('nonexistent_file.json')
    assert result == []

@patch('json.loads', side_effect=json.JSONDecodeError('', '', 0))
def test_read_invalid_json(mock_loads):
    """Тест обработки неправильного формата JSON"""
    result = read_json_file('invalid.json')
    assert result == []
