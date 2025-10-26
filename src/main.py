"""Главный модуль программы."""
from calculator import Calculator
from constants import *


def show_help() -> None:
    """
    Отображает справочную информацию о калькуляторе.

    Показывает список поддерживаемых операций, примеры использования
    и доступные команды интерфейса.
    """
    print(HELP_TEXT)


def format_result(result: float) -> str:
    """
    Форматирует числовой результат для отображения.

    Преобразует float числа с нулевой дробной частью в int формат
    для более читаемого вывода.

    Args:
        result: Числовой результат для форматирования.

    Returns:
        Отформатированная строка представления числа.
    """
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    elif isinstance(result, float):
        return FLOAT_FORMAT.format(result)
    else:
        return str(result)


def main() -> None:
    """
    Основная функция программы.

    Запускает интерактивный цикл обработки пользовательского ввода,
    поддерживает вычисления RPN выражений и команды управления.
    """
    show_help()

    while True:
        try:
            expr = input(PROMPT).strip()

            if expr.lower() == COMMAND_EXIT:
                break

            elif expr.lower() == COMMAND_HELP:
                show_help()
                continue

            calc = Calculator(expr)
            result = calc.eval()
            formatted_result = format_result(result)

            print(formatted_result)

        except KeyboardInterrupt:
            print("\nCtrl+C")

        except EOFError:
            break

        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()