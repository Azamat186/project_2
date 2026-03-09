import json
import logging

from datetime import datetime


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def investment_bank(month: str, transactions: list, limit: int):
    if limit not in [10, 50, 100]:
        raise ValueError("Недопустимый лимит округления.")

    # Проверяем формат месяца
    try:
        if len(month.split('-')) != 2 or not all(map(str.isdigit, month.split('-'))):
            raise ValueError("Неправильный формат месяца")

        year_month = datetime.strptime(month, '%Y-%m')
    except Exception as e:
        logging.error(f"Ошибка при обработке месяца {month}: {e}")
        return None

    total_saved = 0.0

    for transaction in transactions:
        date_str = transaction.get('Date operation', '')
        amount = transaction.get('Amount operation', 0)

        # Проверяем наличие обязательных полей
        if not isinstance(date_str, str) or not isinstance(amount, (float, int)):
            continue

        try:
            trans_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            logging.warning(f"Пропускаем некорректную дату '{date_str}'")
            continue

        # Фильтруем транзакции по месяцу
        if trans_date.year != year_month.year or trans_date.month != year_month.month:
            continue

        # Округляем операцию вверх до ближайшего целого числа кратного заданному лимиту
        rounded_amount = ((amount + limit - 1) // limit) * limit
        saved_amount = rounded_amount - amount

        # Добавляем разницу к общей сумме
        total_saved += saved_amount

    return round(total_saved, 2)


if __name__ == "__main__":
    # Пример использования функции
    transactions_data = [
        {"Date operation": "2023-01-01", "Amount operation": 123},
        {"Date operation": "2023-01-15", "Amount operation": 456},
        {"Date operation": "2023-02-01", "Amount operation": 789},  # Не учитывается, другой месяц
    ]

    result = investment_bank("2023-01", transactions_data, 10)
    print(json.dumps({"result": result}))
