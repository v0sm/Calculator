"""Модуль вычисления RPN выражений."""
from constants import *


class Evaluator:
    """
    Вычислитель для RPN выражений.

    Обрабатывает токены и выполняет операции.
    """

    def __init__(self, tokens: list[str]):
        """
        Инициализирует вычислитель.

        Args:
            tokens: Список токенов для вычисления.
        """
        self.tokens = tokens
        self.i = 0

    def evaluate(self) -> float:
        """
        Вычисляет результат выражения.

        Returns:
            Числовой результат.

        Raises:
            ValueError: Если остались необработанные токены.
        """
        result = self._parse()
        if self.i < len(self.tokens):
            raise ValueError(ERROR_UNPROCESSED_TOKENS)
        return result

    def _parse(self) -> float:
        """
        Парсит токены и вычисляет результат выражения RPN.

        Использует стек для обработки операндов и операторов.
        Поддерживает рекурсивную обработку скобок.

        Returns:
            Результат вычисления выражения.

        Raises:
            ValueError: При некорректной структуре выражения.
        """
        stack = []
        while self.i < len(self.tokens):
            t = self.tokens[self.i]

            if t == OPENING_BRACKET:
                self.i += 1
                res = self._parse()
                stack.append(res)

            elif t == CLOSING_BRACKET:
                self.i += 1
                if len(stack) != 1:
                    if len(stack) == 0:
                        raise ValueError(ERROR_EMPTY_BRACKETS)
                    else:
                        msg = ERROR_INVALID_BRACKET_EXPRESSION.format(len(stack))
                        raise ValueError(msg)
                return stack[0]

            elif t in UNARY_OPERATORS:
                if len(stack) < 1:
                    raise ValueError(ERROR_NOT_ENOUGH_UNARY_ARGS)
                a = stack.pop()
                stack.append(self._calc_unary(a, t))
                self.i += 1

            elif t in BINARY_OPERATORS:
                if len(stack) < 2:
                    raise ValueError(ERROR_NOT_ENOUGH_BINARY_ARGS)
                b = stack.pop()
                a = stack.pop()
                stack.append(self._calc(a, b, t))
                self.i += 1

            else:
                stack.append(self._to_number(t))
                self.i += 1

        if len(stack) != 1:
            msg = ERROR_INVALID_EXPRESSION.format(len(stack))
            raise ValueError(msg)
        return stack[0]

    def _calc(self, a: float, b: float, op: str) -> float:
        """
        Выполняет бинарную арифметическую операцию.

        Args:
            a: Первый операнд.
            b: Второй операнд.
            op: Оператор (+, -, *, /, //, %, **).

        Returns:
            Результат операции.

        Raises:
            ValueError: Если оператор неизвестен.
            ZeroDivisionError: При делении на ноль.
            TypeError: При использовании // или % с нецелыми числами.
        """
        if op == OP_PLUS:
            return a + b
        if op == OP_MINUS:
            return a - b
        if op == OP_MULTIPLY:
            return a * b
        if op == OP_DIVIDE:
            if b == 0:
                raise ZeroDivisionError(ERROR_DIVISION_BY_ZERO)
            return a / b
        if op == OP_POWER:
            return a ** b
        if op == OP_FLOOR_DIV:
            if b == 0:
                raise ZeroDivisionError(ERROR_DIVISION_BY_ZERO)
            if not self._is_integer_value(a) or not self._is_integer_value(b):
                raise TypeError(ERROR_INTEGER_ONLY_FLOOR_DIV)
            return a // b
        if op == OP_MOD:
            if b == 0:
                raise ZeroDivisionError(ERROR_DIVISION_BY_ZERO)
            if not self._is_integer_value(a) or not self._is_integer_value(b):
                raise TypeError(ERROR_INTEGER_ONLY_MOD)
            return a % b
        raise ValueError(ERROR_UNKNOWN_OPERATOR.format(op))

    def _calc_unary(self, a: float, op: str) -> float:
        """
        Выполняет унарную арифметическую операцию.

        Args:
            a: Операнд.
            op: Унарный оператор ($ для +a, ~ для -a).

        Returns:
            Результат унарной операции.

        Raises:
            ValueError: Если унарный оператор неизвестен.
        """
        if op == UNARY_PLUS_SYMBOL:
            return +a
        if op == UNARY_MINUS_SYMBOL:
            return -a
        raise ValueError(ERROR_UNKNOWN_UNARY_OPERATOR.format(op))

    def _to_number(self, token: str) -> float:
        """
        Преобразует строковый токен в число.

        Args:
            token: Строковый токен для преобразования.

        Returns:
            Числовое значение токена (int или float).

        Raises:
            ValueError: Если токен не является корректным числом.
        """
        if POINT in token:
            try:
                return float(token)
            except ValueError:
                raise ValueError(ERROR_INVALID_NUMBER.format(token))
        if token.lstrip(PLUS_MINUS).isdigit():
            return int(token)
        raise ValueError(ERROR_INVALID_NUMBER.format(token))

    def _is_integer_value(self, num: float) -> bool:
        """
        Проверяет, является ли число целым по значению.

        Учитывает float числа вида 5.0 как целые.

        Args:
            num: Число для проверки.

        Returns:
            True если число является целым по значению.
        """
        if isinstance(num, int):
            return True
        if isinstance(num, float):
            return num.is_integer()
        return False
