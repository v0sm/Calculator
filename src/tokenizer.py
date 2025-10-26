"""Модуль токенизации выражений."""
from constants import *


class Tokenizer:
    """
    Лексический анализатор для RPN выражений.

    Преобразует строку в список токенов.
    """

    def __init__(self, expression: str):
        """
        Инициализирует токенизатор.

        Args:
            expression: Строка с выражением.
        """
        self.expr = expression

    def tokenize(self) -> list[str]:
        """
        Разбивает выражение на токены.

        Returns:
            Список токенов.

        Raises:
            ValueError: При некорректном выражении.
        """
        if not self.expr.strip():
            raise ValueError(ERROR_EMPTY_EXPRESSION)

        if not self._check_brackets():
            raise ValueError(ERROR_UNBALANCED_BRACKETS)

        return self._parse_tokens()

    def _check_brackets(self) -> bool:
        """
        Проверяет баланс скобок.

        Returns:
            True если скобки сбалансированы, False иначе.
        """
        count = 0
        for char in self.expr:
            if char == OPENING_BRACKET:
                count += 1
            elif char == CLOSING_BRACKET:
                count -= 1
                if count < 0:
                    return False
        return count == 0

    def _parse_tokens(self) -> list[str]:
        """
        Парсит токены из строки.

        Returns:
            Список токенов.

        Raises:
            ValueError: При некорректных символах или числах.
        """
        tokens = []
        i = 0
        length = len(self.expr)

        while i < length:
            char = self.expr[i]

            if char.isspace():
                i += 1
                continue

            elif char in BRACKETS:
                tokens.append(char)
                i += 1
                continue

            if char in UNARY_OPERATORS:
                tokens.append(char)
                i += 1
                continue

            if char == OP_MULTIPLY and i + 1 < length and self.expr[i + 1] == OP_MULTIPLY:
                tokens.append(OP_POWER)
                i += 2
                continue

            if char == OP_DIVIDE and i + 1 < length and self.expr[i + 1] == OP_DIVIDE:
                tokens.append(OP_FLOOR_DIV)
                i += 2
                continue

            if char in SINGLE_CHAR_BINARY_OPERATORS:
                tokens.append(char)
                i += 1
                continue

            if char.isdigit() or char == POINT:
                start = i

                while i < length and self.expr[i].isdigit():
                    i += 1

                if i < length and self.expr[i] == POINT:
                    i += 1
                    while i < length and self.expr[i].isdigit():
                        i += 1

                number_str = self.expr[start:i]
                if self._is_valid_number(number_str):
                    tokens.append(number_str)
                else:
                    raise ValueError(ERROR_INVALID_NUMBER.format(number_str))
                continue

            if char in PLUS_MINUS:
                if (i + 1 < length and
                        (self.expr[i + 1].isdigit() or self.expr[i + 1] == POINT) and
                        self._is_start_of_number_context(tokens)):

                    start = i
                    i += 1

                    while i < length and self.expr[i].isdigit():
                        i += 1

                    if i < length and self.expr[i] == POINT:
                        i += 1
                        while i < length and self.expr[i].isdigit():
                            i += 1

                    number_str = self.expr[start:i]
                    if self._is_valid_number(number_str):
                        tokens.append(number_str)
                    else:
                        raise ValueError(ERROR_INVALID_NUMBER.format(number_str))
                    continue
                else:
                    tokens.append(char)
                    i += 1
                    continue

            raise ValueError(ERROR_UNKNOWN_SYMBOL.format(char))

        if not tokens:
            raise ValueError(ERROR_NO_TOKENS)

        return tokens

    def _is_valid_number(self, num_str: str) -> bool:
        """
        Проверяет корректность строкового представления числа.

        Args:
            num_str: Строка для проверки.

        Returns:
            True если строка является корректным числом.
        """
        if not num_str:
            return False

        if num_str[0] in PLUS_MINUS:
            num_str = num_str[1:]

        if not num_str:
            return False

        try:
            float(num_str)
            return True
        except ValueError:
            return False

    def _is_start_of_number_context(self, tokens: list[str]) -> bool:
        """
        Определяет, может ли +/- быть началом числа в данном контексте.

        Args:
            tokens: Список уже распознанных токенов.

        Returns:
            True если +/- может быть началом числа.
        """
        if not tokens:
            return True

        last_token = tokens[-1]

        if (last_token == OPENING_BRACKET or
            last_token in BINARY_OPERATORS or
            last_token in UNARY_OPERATORS):
            return True

        return False
