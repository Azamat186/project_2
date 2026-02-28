import os

from typing import Dict, Optional

import requests


def convert_to_rubles(transaction: Dict[str, any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли, используя внешний API.
    Для валют USD и EUR обращается к стороннему API для конвертации.

    :param transaction: словарь с информацией о транзакции
    :type transaction: dict
    :returns: сумма в рублях или None в случае ошибки
    :rtype: float | None
    """
    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if not amount or not currency:
        return None

    # Непосредственно конвертируем, если валюта уже рубли
    if currency == "RUB":
        return float(amount)

    # Только USD и EUR требуют конвертацию
    elif currency in ["USD", "EUR"]:
        # Получаем ключ API из окружения
        api_key = os.getenv("EXCHANGE_RATES_DATA_API_KEY")

        # Отправляем запрос к API для конвертации указанной суммы в рубли
        response = requests.get(
            f"https://api.apilayer.com/currency_data/convert?to=RUB&from={currency}&amount={amount}",
            headers={"apikey": api_key},
        )

        if response.status_code == 200:
            data = response.json()
            converted_amount = data.get("result")

            # Проверяем наличие значения перед преобразованием
            if converted_amount is not None:
                return round(float(converted_amount), 2)

    return None
