from datetime import datetime


def filter_by_state(transactions, state='EXECUTED'):
    """ Фильтрует транзакции по состоянию. :param transactions: Список словарей с операциями :param state:
     Статус операций ('EXECUTED' по умолчанию) :return: Отфильтрованный список операций """
    return [t for t in transactions if t.get('state') == state]


def sort_by_date(transactions, ascending=False):
    """ Сортирует операции по дате. :param transactions: Список словарей с операциями :param ascending:
     Если True, сортируем по возрастанию дат (по умолчанию False) :return: Отсортированный список операций """
    sorted_transactions = sorted(
        transactions,
        key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
        reverse=True
    )
    return sorted_transactions

transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-07-01'},
    {'id': 2, 'state': 'CANCELED', 'date': '2023-07-02'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2023-07-03'}
]

filtered_transactions = filter_by_state(transactions)
print(filtered_transactions)
#

sorted_transactions = sort_by_date(transactions)
print(sorted_transactions)
