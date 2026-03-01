import csv
import json
import re
from datetime import datetime
import pandas as pd
from collections import Counter


# Функции загрузки данных из различных источников
def load_json(filename="transactions.json"):
    """Загрузка данных из JSON"""
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return []


def load_csv(filename="transactions.csv"):
    """Загрузка данных из CSV"""
    try:
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return []


def load_xlsx(filename="transactions.xlsx"):
    """Загрузка данных из XLSX"""
    try:
        df = pd.read_excel(filename, engine='openpyxl')
        return df.to_dict('records')
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return []


# Основные рабочие функции
def sort_by_date(transactions):
    """Сортирует транзакции по дате в порядке возрастания."""
    sorted_transactions = sorted(
        transactions,
        key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'),
        reverse=False
    )
    return sorted_transactions


def filter_by_currency(transactions, currency='RUB'):
    """Отбирает только транзакции заданной валюты."""
    filtered_transactions = [
        t for t in transactions
        if t.get('currency') and t['currency'] == currency
    ]
    return filtered_transactions


def filter_by_description(transactions, keyword=None):
    """Фильтрует транзакции по наличию ключевого слова в поле описания."""
    if keyword is None or keyword.strip() == '':
        return transactions
    else:
        filtered_transactions = [
            t for t in transactions
            if keyword.lower() in str(t.get('description')).lower()
        ]
        return filtered_transactions


def display_transactions(transactions):
    """Выводит на экран перечень всех транзакций в удобочитаемом виде."""
    for idx, trans in enumerate(transactions):
        date_str = trans.get('date', '')
        description = trans.get('description', '')
        account_from = trans.get('account_from', '')
        account_to = trans.get('account_to', '')
        amount = trans.get('amount', '')
        currency = trans.get('currency', '')

        print(f"{idx + 1}. Дата: {date_str}")
        print(f"   Описание: {description}")
        print(f"   Отправитель: {account_from}")
        print(f"   Получатель: {account_to}")
        print(f"   Сумма: {amount} {currency}\n")


def search_by_keyword(transactions, keyword):
    """
    Фильтрует транзакции по наличию ключевого слова в поле описания.

    :param transactions: Список транзакций
    :param keyword: Ключевое слово для поиска
    :return: Отфильтрованный список транзакций
    """
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return [trans for trans in transactions if pattern.search(str(trans.get('description')))]


def count_operations_by_category(transactions):
    """
    Подсчитывает количество операций по каждой категории с использованием Counter.

    :param transactions: Список транзакций
    :return: Словарь с категориями и количеством операций
    """
    categories = [trans.get('category', 'Без категории') for trans in transactions]
    return dict(Counter(categories))


# Основной рабочий цикл программы
def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("Ваш выбор: ").strip()

        if choice not in ['1', '2', '3']:
            print("Ошибка: выберите номер от 1 до 3.")
            continue

        break

    # Выбор нужной функции загрузки файлов в зависимости от выбора пользователя
    file_loaders = {
        '1': load_json,
        '2': load_csv,
        '3': load_xlsx
    }

    loader_function = file_loaders.get(choice)
    transactions = loader_function()  # Загружаем реальные данные из выбранного файла

    if len(transactions) == 0:
        print("Нет данных для обработки.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]  # Допустимые статусы операций

    while True:
        status_input = input(f"Введите статус ({', '.join(valid_statuses)}): ").upper().strip()

        if status_input in valid_statuses:
            filtered_transactions = [
                transaction for transaction in transactions
                if transaction.get('status') == status_input
            ]

            print(f"Транзакций со статусом {status_input}: {len(filtered_transactions)}\n")
            break
        else:
            print(f"Статус '{status_input}' недоступен.")

    # Проверка наличия хотя бы одной транзакции
    if len(filtered_transactions) > 0:
        # Дополнительные фильтры и сортировка
        need_sorting = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
        if need_sorting.startswith('д') or need_sorting.startswith('y'):
            sort_order = input("Отсортировать по возрастанию или по убыванию? (возрастание/убывание): ").strip().lower()
            if sort_order.startswith('у') or sort_order.startswith('d'):  # Убывание
                filtered_transactions.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
            else:  # Возрастание
                filtered_transactions.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'))

        ruble_filter = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
        if ruble_filter.startswith('д') or ruble_filter.startswith('y'):
            filtered_transactions = filter_by_currency(filtered_transactions, 'RUB')

        keyword_filter = input(
            "Отфильтровать список транзакций по определённому слову в описании? Да/Нет: ").strip().lower()
        if keyword_filter.startswith('д') or keyword_filter.startswith('y'):
            keyword = input("Введите слово для фильтрации: ")
            filtered_transactions = filter_by_description(filtered_transactions, keyword)

        # Если список пуст после фильтров
        if len(filtered_transactions) == 0:
            print("Не найдено ни одной транзакции, соответствующей вашим условиям фильтрации.")
        else:
            print("\nРаспечатываю итоговый список транзакций...")
            display_transactions(filtered_transactions)
    else:
        print("Не найдено ни одной транзакции с указанным вами статусом.")

    # Дополнительные возможности
    while True:
        print("\nДополнительные возможности:")
        print("1. Найти транзакции по ключевым словам")
        print("2. Посмотреть распределение операций по категориям")
        action_choice = input("Ваш выбор: ").strip()

        if action_choice == '1':
            keyword = input("Введите ключевое слово для поиска: ")
            found_transactions = search_by_keyword(filtered_transactions, keyword)
            if len(found_transactions) > 0:
                print(f"\nНайдено {len(found_transactions)} транзакций по запросу '{keyword}'.")
                display_transactions(found_transactions)
            else:
                print(f"Ничего не найдено по вашему запросу '{keyword}'.")

        elif action_choice == '2':
            category_counts = count_operations_by_category(filtered_transactions)
            print("\nКатегории и количество операций:\n")
            for cat, count in category_counts.items():
                print(f"- Категория: {cat}, Количество: {count}")

        else:
            print("Неправильный ввод. Повторите попытку.")


if __name__ == "__main__":
    main()
