import logging
import os
from pathlib import Path
from typing import Union, List, Dict
import json


# Создание логера для модуля utils
logger_utils = logging.getLogger("utils")
logger_utils.setLevel(logging.DEBUG)

# Определение пути к директории logs
log_dir = Path(__file__).parent.parent / "logs"
os.makedirs(log_dir, exist_ok=True)

# Форматтер сообщений лога
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Обработчик файла для log-потоков
file_handler = logging.FileHandler(os.path.join(log_dir, "utils.log"), mode="w")
file_handler.setFormatter(formatter)

# Добавляем хэндлер в логгер
logger_utils.addHandler(file_handler)


def read_json_file(file_path: str) -> Union[List[Dict], List]:
    """
    Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях.
    Если файл не существует, пустой или содержит неправильные данные, возвращает пустой список.

    :param file_path: путь к файлу JSON
    :type file_path: str
    :rtype: list
    """
    logger_utils.debug(f"Чтение файла {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transactions = json.load(f)

        # Проверяем, что данные представляют собой список
        if isinstance(transactions, list):
            logger_utils.info(f"Файл успешно прочитан, количество транзакций: {len(transactions)}")
            return transactions
        else:
            logger_utils.error("Ошибка формата данных: ожидается список транзакций.")
            return []

    except FileNotFoundError:
        logger_utils.error(f'Ошибка: файл "{file_path}" не найден.')
        return []
    except json.JSONDecodeError:
        logger_utils.error(f'Ошибка: некорректный формат JSON в файле "{file_path}".')
        return []
