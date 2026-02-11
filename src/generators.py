def filter_by_currency(transactions, currency_code):
    """
    Возвращает итератор, включающий только транзакции с указанным кодом валюты.

    :param transactions: Список словарей с транзакциями.
    :param currency_code: Код валюты ("USD", "EUR" и т.д.).
    :return: Итератор с соответствующими транзакциями.
    """
    return (tx for tx in transactions if tx.get('operationAmount', {}).get('currency', {}).get('code') == currency_code)


def transaction_descriptions(transactions):
    """
    Генератор, возвращающий описание каждой транзакции по порядку.

    :param transactions: Список словарей с транзакциями.
    :return: Итератор с описаниями транзакций.
    """
    return (tx.get('description') for tx in transactions)


def card_number_generator(start=1, end=9999999999999999):
    """
    Генератор банковских карточных номеров в формате XXXX XXXX XXXX XXXX.

    :param start: Начальная карта.
    :param end: Конечная карта.
    :return: Итератор с номерами карт.
    """
    format_str = "{:016d}"  # Формат строки с шестнадцатью цифрами
    for i in range(start, end+1):  # Включаем последнюю карту в генерацию
        formatted_number = format_str.format(i)
        # Разбиваем строку на блоки по 4 символа
        blocks = [formatted_number[i:i+4] for i in range(0, len(formatted_number), 4)]
        yield " ".join(blocks)


