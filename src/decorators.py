import functools
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования деталей выполнения функций,
    включая время вызова, имя функции, передаваемые аргументы, результат выполнения и информацию об ошибках.

    :param filename: Имя файла для записи логов. Если None, логи выводятся в консоль.
    :return: Обернутую функцию с поддержкой логирования.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__}: {result}"
                if filename is not None:
                    with open(filename, 'a') as file:
                        file.write(message + '\n')
                else:
                    print(message)
                return result
            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename is not None:
                    with open(filename, 'a') as file:
                        file.write(error_message + '\n')
                else:
                    print(error_message)
                raise

        return wrapper

    return decorator
