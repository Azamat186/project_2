import pytest
from src.decorators import log


def test_log_to_console_success(capsys):  # Здесь capsys берётся из pytest
    # Функция, которую будем декорировать
    @log()
    def add(a, b):
        return a + b

    # Проверяем успешное выполнение функции
    assert add(1, 2) == 3
    captured = capsys.readouterr()  # Читаем захваченный вывод
    output = captured.out.strip()  # Забираем вывод из out
    expected_output = "add: 3"
    assert output == expected_output


def test_log_to_file_success(tmp_path):
    temp_file = tmp_path / "test.log"
    @log(str(temp_file))
    def multiply(a, b):
        """Multiply two numbers."""
        return a * b

    multiply(3, 4)
    with open(temp_file, 'r') as f:
        content = f.read().strip()
    expected_output = "multiply: 12"
    assert content == expected_output


def test_log_to_console_error(capsys):  # И здесь capsys берется из pytest
    @log()
    def divide(a, b):
        """Divide two numbers."""
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    captured = capsys.readouterr()  # Читаем захваченный вывод
    output = captured.out.strip()  # Забираем вывод из out
    expected_output = "divide error: ZeroDivisionError. Inputs: (1, 0), {}"
    assert output == expected_output


def test_log_to_file_error(tmp_path):
    temp_file = tmp_path / "test.log"
    @log(str(temp_file))
    def subtract(a, b):
        """Subtract one number from another."""
        if a > b:
            raise ValueError("A must be less than B.")
        return a - b

    with pytest.raises(ValueError):
        subtract(5, 3)
    with open(temp_file, 'r') as f:
        content = f.read().strip()
    expected_output = "subtract error: ValueError. Inputs: (5, 3), {}"
    assert content == expected_output
