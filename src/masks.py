import logging
import os
from pathlib import Path
from typing import Union
import re

# Создаем логгер для модуля masks
logger_masks = logging.getLogger('masks')
logger_masks.setLevel(logging.DEBUG)

# Определяем каталог для хранения логов
log_dir = Path(__file__).parent.parent / 'logs'
os.makedirs(log_dir, exist_ok=True)

# Устанавливаем формат сообщений лога
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Хэндлер для обработки логов в файл
file_handler = logging.FileHandler(os.path.join(log_dir, 'masks.log'), mode='w')
file_handler.setFormatter(formatter)

# Регистрация хэндлера
logger_masks.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """ Получает число с номером кредитной карты и формирует её маску вида XXXX XX** **** XXXX.
     Первая шестерка символов видима, последние четыре также остаются открытыми, остальное скрыто символом '*'.
      Блокировка идет каждые четыре символа. Args: card_number (int): Номер кредитной карты длиной ровно 16 цифр.
       Raises: ValueError: Если длина не равна 16 или карта содержит недопустимые символы. Returns: str:
       Маскированная строка номера карты. """
    card_str = str(card_number)
    if len(card_str) != 16 or not card_str.isdigit():
        logger_masks.error(f'Некорректный формат номера карты: {card_number}.')
        raise ValueError("Неверный формат номера карты.")

    blocks = re.findall(r'\d{4}', card_str)
    masked_blocks = [blocks[0], blocks[1][:2] + "**", "****", blocks[-1]]
    result = " ".join(masked_blocks)
    logger_masks.info(f'Карточка замаскирована: {result}')
    return result


def get_mask_account(account_number: Union[int, str]) -> str:
    """ Формирует маску банковского счёта вида **XXXX, показывая только последнюю четверку символов. Args:
    account_number (Union[int, str]): Номер банковского счёта длиной больше или равной 4 цифрам. Raises: ValueError:
     Если счёт короче четырёх символов или содержит нецифровые символы. Returns: str:
     Маскированная строка номера счёта. """
    acc_str = str(account_number)
    if len(acc_str) < 4 or not acc_str.isdigit():
        logger_masks.error(f'Некорректный формат счета: {account_number}.')
        raise ValueError("Неверный формат номера счета.")

    result = f"**{acc_str[-4:]}"
    logger_masks.info(f'Cчёт замаскирован: {result}')
    return result

