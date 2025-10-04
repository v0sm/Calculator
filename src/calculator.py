class Calculator:
    """
    Калькулятор для обратной польской нотации (RPN).

    Принимает строковые выражения в RPN формате и вычисляет их значения.
    Поддерживает базовые арифметические операции, унарные операторы и скобки.

    Attributes:
        tokens (list): Список токенов после предобработки выражения.
        i (int): Текущая позиция в списке токенов.
    """
    def __init__(self, expr):
        """
        Инициализирует калькулятор с выражением.

        Args:
            expr (str): Выражение в формате RPN для вычисления.

        Raises:
            ValueError: Если выражение пустое или не содержит токенов.
        """
        if not expr.strip():
            raise ValueError('Пустое выражение')
        self.tokens = self._preprocess(expr)
        self.i = 0

    def _preprocess(self, expr):
        """
        Лексический анализатор: преобразует строку в список токенов.

        Поддерживает разбор выражений без пробелов между операторами и операндами.
        Распознает числа, операторы, скобки и унарные операторы.
        """
        if not self._check_brackets(expr):
            raise ValueError('Несбалансированные скобки')

        tokens = []
        i = 0
        length = len(expr)

        while i < length:
            char = expr[i]

            if char.isspace():
                i += 1
                continue

            if char in '()':
                tokens.append(char)
                i += 1
                continue

            if char in '~$':
                tokens.append(char)
                i += 1
                continue

            if char == '*' and i + 1 < length and expr[i + 1] == '*':
                tokens.append('**')
                i += 2
                continue

            if char == '/' and i + 1 < length and expr[i + 1] == '/':
                tokens.append('//')
                i += 2
                continue

            if char in '+-*/%':
                tokens.append(char)
                i += 1
                continue

            if char.isdigit() or char == '.':
                start = i

                while i < length and expr[i].isdigit():
                    i += 1

                if i < length and expr[i] == '.':
                    i += 1
                    while i < length and expr[i].isdigit():
                        i += 1

                number_str = expr[start:i]
                if self._is_valid_number(number_str):
                    tokens.append(number_str)
                else:
                    raise ValueError(f'Некорректное число: {number_str}')
                continue

            if char in '+-':
                # Проверяем, является ли это началом числа
                if (i + 1 < length and
                        (expr[i + 1].isdigit() or expr[i + 1] == '.') and
                        self._is_start_of_number_context(tokens)):

                    start = i
                    i += 1

                    while i < length and expr[i].isdigit():
                        i += 1

                    if i < length and expr[i] == '.':
                        i += 1
                        while i < length and expr[i].isdigit():
                            i += 1

                    number_str = expr[start:i]
                    if self._is_valid_number(number_str):
                        tokens.append(number_str)
                    else:
                        raise ValueError(f'Некорректное число: {number_str}')
                    continue
                else:
                    tokens.append(char)
                    i += 1
                    continue

            # Неизвестный символ
            raise ValueError(f'Неизвестный символ: {char}')

        if not tokens:
            raise ValueError('Выражение не содержит токенов')

        return tokens

    @staticmethod
    def _is_valid_number(num_str):
        """Проверяет корректность строкового представления числа."""
        if not num_str:
            return False

        if num_str[0] in '+-':
            num_str = num_str[1:]

        if not num_str:
            return False

        try:
            float(num_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_start_of_number_context(tokens):
        """Определяет, может ли +/- быть началом числа в данном контексте."""
        if not tokens:
            return True

        last_token = tokens[-1]

        if last_token in ('(', '+', '-', '*', '/',
                          '//', '**', '%', '~', '$'):
            return True

        return False

    @staticmethod
    def _check_brackets(expr):
        """
        Проверяет сбалансированность скобок в выражении.

        Args:
            expr (str): Выражение для проверки.

        Returns:
            bool: True если скобки сбалансированы, False в противном случае.
        """
        count = 0
        for char in expr:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0

    @staticmethod
    def _to_number(token):
        """
        Преобразует строковый токен в число.

        Args:
            token (str): Строковый токен для преобразования.

        Returns:
            int or float: Числовое значение токена.

        Raises:
            ValueError: Если токен не является корректным числом.
        """
        if '.' in token:
            try:
                return float(token)
            except ValueError:
                raise ValueError(f'Некорректное число: {token}')
        if token.lstrip('+-').isdigit():
            return int(token)
        raise ValueError(f'Некорректное число: {token}')

    @staticmethod
    def _is_integer_value(num):
        """
        Проверяет, является ли число целым по значению.

        Учитывает float числа вида 5.0 как целые.

        Args:
            num (int or float): Число для проверки.

        Returns:
            bool: True если число является целым по значению.
        """
        if isinstance(num, int):
            return True
        if isinstance(num, float):
            return num.is_integer()
        return False

    @staticmethod
    def _calc(a, b, op):
        """
        Выполняет бинарную арифметическую операцию.

        Args:
            a (int or float): Первый операнд.
            b (int or float): Второй операнд.
            op (str): Оператор (+, -, *, /, //, %, **).

        Returns:
            int or float: Результат операции.

        Raises:
            ValueError: Если оператор неизвестен.
            ZeroDivisionError: При делении на ноль.
            TypeError: При использовании // или % с нецелыми числами.
        """
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError('Деление на ноль')
            return a / b
        if op == '**':
            return a ** b
        if op == '//':
            if b == 0:
                raise ZeroDivisionError('Деление на ноль')
            if not Calculator._is_integer_value(a) or not Calculator._is_integer_value(b):
                raise TypeError('Операция // только для целых чисел')
            return a // b
        if op == '%':
            if b == 0:
                raise ZeroDivisionError('Деление на ноль')
            if not Calculator._is_integer_value(a) or not Calculator._is_integer_value(b):
                raise TypeError('Операция % только для целых чисел')
            return a % b
        raise ValueError(f'Неизвестный оператор: {op}')

    @staticmethod
    def _calc_unary(a, op):
        """
        Выполняет унарную арифметическую операцию.

        Args:
            a (int or float): Операнд.
            op (str): Унарный оператор ($ для +a, ~ для -a).

        Returns:
            int or float: Результат унарной операции.

        Raises:
            ValueError: Если унарный оператор неизвестен.
        """
        if op == '$':
            return +a
        if op == '~':
            return -a
        raise ValueError(f'Неизвестный унарный оператор: {op}')

    def _parse(self):
        """
        Парсит токены и вычисляет результат выражения RPN.

        Использует стек для обработки операндов и операторов.
        Поддерживает рекурсивную обработку скобок.

        Returns:
            int or float: Результат вычисления выражения.

        Raises:
            ValueError: При некорректной структуре выражения.
        """
        stack = []
        while self.i < len(self.tokens):
            t = self.tokens[self.i]
            if t == '(':
                self.i += 1
                res = self._parse()
                stack.append(res)
            elif t == ')':
                self.i += 1
                if len(stack) != 1:
                    if len(stack) == 0:
                        raise ValueError('Пустые скобки')
                    else:
                        msg = (f'Некорректное выражение в скобках: '
                               f'осталось {len(stack)} элементов вместо 1')
                        raise ValueError(msg)
                return stack[0]
            elif t in {'$', '~'}:
                if len(stack) < 1:
                    msg = 'Недостаточно аргументов для унарного оператора'
                    raise ValueError(msg)
                a = stack.pop()
                stack.append(self._calc_unary(a, t))
                self.i += 1
            elif t in {'+', '-', '*', '/', '**', '//', '%'}:
                if len(stack) < 2:
                    msg = 'Недостаточно аргументов для бинарного оператора'
                    raise ValueError(msg)
                b = stack.pop()
                a = stack.pop()
                stack.append(self._calc(a, b, t))
                self.i += 1
            else:
                stack.append(self._to_number(t))
                self.i += 1

        if len(stack) != 1:
            msg = (f'Некорректное выражение: '
                   f'осталось {len(stack)} элементов в стеке')
            raise ValueError(msg)
        return stack[0]

    def eval(self):
        """
        Вычисляет значение RPN выражения.

        Основной публичный интерфейс для получения результата вычислений.

        Returns:
            int or float: Числовой результат вычисления выражения.

        Raises:
            ValueError: При наличии необработанных токенов после парсинга.
        """
        result = self._parse()
        if self.i < len(self.tokens):
            raise ValueError('Остались необработанные токены')
        return result
