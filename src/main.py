from calculator import Calculator


def show_help():
    """
    Отображает справочную информацию о калькуляторе.

    Показывает список поддерживаемых операций, примеры использования
    и доступные команды интерфейса.
    """
    print("\nRPN Калькулятор")
    print("Операции: +, -, *, /, //, %, **")
    print("Унарные: ~ (минус), $ (плюс)")
    print("Примеры: 3 4 +, 5 ~, 2 ( 3 4 + ) *")
    print("Команды: help, exit")


def format_result(result):
    """
    Форматирует числовой результат для отображения.

    Преобразует float числа с нулевой дробной частью в int формат
    для более читаемого вывода.

    Args:
        result (int or float): Числовой результат для форматирования.

    Returns:
        str: Отформатированная строка представления числа.
    """
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    elif isinstance(result, float):
        return f"{result:.6g}"
    else:
        return str(result)


def main():
    """
    Основная функция программы.

    Запускает интерактивный цикл обработки пользовательского ввода,
    поддерживает вычисления RPN выражений и команды управления.
    """
    show_help()

    while True:
        try:
            expr = input("\nRPN> ").strip()

            if expr.lower() == 'exit':
                break

            elif expr.lower() == 'help':
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
