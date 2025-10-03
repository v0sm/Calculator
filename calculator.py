class Calculator:
    def __init__(self, expr):
        if not expr.strip():
            raise ValueError('Пустое выражение')
        self.tokens = self._preprocess(expr)
        self.i = 0

    def _preprocess(self, expr):
        if not self._check_brackets(expr):
            raise ValueError('Несбалансированные скобки')

        result = ""
        for char in expr:
            if char in '()':
                result += f' {char} '
            else:
                result += char

        tokens = result.split()
        if not tokens:
            raise ValueError('Выражение не содержит токенов')

        return tokens

    @staticmethod
    def _check_brackets(expr):
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
        if '.' in token:
            try:
                return float(token)
            except ValueError:
                raise ValueError(f'Некорректное число: {token}')
        if token.lstrip('+-').isdigit():
            return int(token)
        raise ValueError(f'Некорректное число: {token}')

    @staticmethod
    def _calc(a, b, op):
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
            if not isinstance(a, int) or not isinstance(b, int):
                raise TypeError('Операция только для целых чисел')
            return a // b
        if op == '%':
            if b == 0:
                raise ZeroDivisionError('Деление на ноль')
            if not isinstance(a, int) or not isinstance(b, int):
                raise TypeError('Операция только для целых чисел')
            return a % b
        raise ValueError(f'Неизвестный оператор: {op}')

    @staticmethod
    def _calc_unary(a, op):
        if op == '$':
            return +a
        if op == '~':
            return -a
        raise ValueError(f'Неизвестный унарный оператор: {op}')

    def _parse(self):
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
                        raise ValueError(f'Некорректное выражение в скобках: осталось {len(stack)} элементов вместо 1')
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
            raise ValueError(f'Некорректное выражение: осталось {len(stack)} элементов в стеке')
        return stack[0]

    def eval(self):
        result = self._parse()
        if self.i < len(self.tokens):
            raise ValueError('Остались необработанные токены')
        return result
