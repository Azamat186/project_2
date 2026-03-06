Описание проекта
Проект предназначен для автоматизации сбора, обработки и анализа данных о банковских транзакциях. Он позволяет:

получать данные о транзакциях через API банка;

сохранять и структурировать данные в разных форматах;

проводить первичный анализ и статистику по транзакциям;

вести логирование операций для отладки и аудита.

Используемые библиотеки и их роль
1. Библиотеки json, requests и datetime
Назначение: получение и обработка данных о транзакциях.

requests: используется для отправки HTTP‑запросов к API банка и получения данных о транзакциях в формате JSON.

json: позволяет парсить JSON‑ответы от API и преобразовывать их в структуры данных Python (словари, списки).

datetime: обеспечивает работу с датами и временем — фильтрацию транзакций по периоду, форматирование дат в отчётах.

Пример использования:

python
import requests
import json
from datetime import datetime

# Отправка запроса к API
response = requests.get('https://api.bank.com/transactions', params={'start_date': '2023-01-01'})

# Парсинг JSON-ответа
transactions = json.loads(response.text)

# Фильтрация транзакций за последний месяц
current_date = datetime.now()
recent_transactions = [
    t for t in transactions
    if datetime.fromisoformat(t['date']) >= current_date - timedelta(days=30)
]
2. Библиотека logging
Назначение: ведение журнала операций для отслеживания работы программы и отладки.

Позволяет:

записывать сообщения разного уровня важности (DEBUG, INFO, WARNING, ERROR, CRITICAL);

сохранять логи в файл или выводить в консоль;

настраивать формат и детализацию логов.

Пример настройки:

python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transactions.log'),
        logging.StreamHandler()
    ]
)

logging.info('Начало обработки транзакций')
logging.error('Ошибка при получении данных от API')
3. Библиотеки csv и pandas
Назначение: сохранение и анализ данных.

csv: простая запись и чтение данных в формате CSV — подходит для экспорта транзакций в таблицы (Excel, Google Sheets).

pandas: мощная библиотека для анализа данных: фильтрация, группировка, агрегация, визуализация.

Примеры:

Запись в CSV:

python
import csv

with open('transactions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'amount', 'description'])
    writer.writeheader()
    writer.writerows(transactions)
Анализ с pandas:

python
import pandas as pd

df = pd.DataFrame(transactions)
total_spent = df[df['amount'] < 0]['amount'].sum()  # Общие расходы
top_categories = df.groupby('category')['amount'].sum().nlargest(5)  # Топ-5 категорий
4. Библиотеки re, collections, random
Назначение: дополнительная обработка и генерация данных.

re (Regular Expressions): поиск и извлечение информации из текстовых полей (например, выделение номеров счетов или кодов операций из описания транзакции).

collections: структуры данных для эффективной обработки (например, Counter для подсчёта частоты категорий транзакций).

random: генерация тестовых данных (например, для отладки без доступа к реальному API).

Примеры:

Использование re:

python
import re

# Извлечение номера счёта из описания
description = "Перевод на счёт 40702810000000001234"
account_number = re.search(r'\b\d{20}\b', description).group()
Использование collections:

python
from collections import Counter

# Подсчёт частоты категорий транзакций
category_counts = Counter(t['category'] for t in transactions)
print(category_counts.most_common(3))  # Топ-3 категории
Использование random:

python
import random

# Генерация тестовых транзакций
test_transactions = [
    {
        'date': f'2023-01-{random.randint(1, 31):02d}',
        'amount': random.uniform(-1000, 5000),
        'description': 'Test transaction'
    }
    for _ in range(10)
]
Как запустить проект
Установите зависимости:

bash
pip install pandas requests
Настройте параметры API (URL, токен) в файле config.py.

Запустите основной скрипт:

bash
python main.py
Результаты будут сохранены в:

transactions.csv — все транзакции;

report.xlsx — аналитический отчёт (если используется pandas);

transactions.log — журнал операций.

Структура проекта
project/
├── main.py              # Основной скрипт
├── config.py            # Настройки API и путей
├── data/                # Папка для данных
│   ├── transactions.csv # Экспорт транзакций
│   └── report.xlsx     # Аналитический отчёт
├── logs/
│   └── transactions.log # Журнал операций
└── README.md            # Эта документация