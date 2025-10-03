from calculator import Calculator


def show_help():
    print("\nRPN Калькулятор")
    print("Операции: +, -, *, /, //, %, **")
    print("Унарные: ~ (минус), $ (плюс)")
    print("Примеры: 3 4 +, 5 ~, 2 ( 3 4 + ) *")
    print("Команды: help, exit, history")


def format_result(result):
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    elif isinstance(result, float):
        return f"{result:.6g}"
    else:
        return str(result)


def main():
    show_help()
    history = []

    while True:
        try:
            expr = input("\nRPN> ").strip()

            if expr.lower() == 'exit':
                break

            elif expr.lower() == 'help':
                show_help()
                continue

            elif expr.lower() == 'history':
                for i, (expression, result) in enumerate(history[-10:], 1):
                    print(f"{i:2}. {expression} = {result}")
                continue

            calc = Calculator(expr)
            result = calc.eval()
            formatted_result = format_result(result)

            print(formatted_result)

            history.append((expr, formatted_result))

            if len(history) > 50:
                history.pop(0)

        except KeyboardInterrupt:
            print("\nCtrl+C")

        except EOFError:
            break

        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
