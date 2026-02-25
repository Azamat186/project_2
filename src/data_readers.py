import pandas as pd
from typing import List, Dict


def read_csv_transactions(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из файла формата CSV и возвращает список словарей,
    каждый из которых представляет одну операцию.

    :param file_path: Путь к файлу CSV
    :return: Список словарей с операциями
    """
    df = pd.read_csv(file_path)
    return df.to_dict("records")


def read_excel_transactions(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из файла формата Excel (.xls/.xlsx) и возвращает список словарей,
    каждый из которых представляет одну операцию.

    :param file_path: Путь к файлу Excel
    :return: Список словарей с операциями
    """
    df = pd.read_excel(file_path)
    return df.to_dict("records")
