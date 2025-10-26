"""Константы для калькулятора."""

# Операторы
OP_PLUS = '+'
OP_MINUS = '-'
OP_MULTIPLY = '*'
OP_DIVIDE = '/'
OP_POWER = '**'
OP_FLOOR_DIV = '//'
OP_MOD = '%'
BINARY_OPERATORS = {OP_PLUS, OP_MINUS, OP_MULTIPLY, OP_DIVIDE, OP_POWER, OP_FLOOR_DIV, OP_MOD}
SINGLE_CHAR_BINARY_OPERATORS = '+-*/%'
UNARY_OPERATORS = {'~', '$'}
PLUS_MINUS = '+-'
ALL_OPERATORS = BINARY_OPERATORS | UNARY_OPERATORS

# Двухсимвольные операторы (для парсинга)
DOUBLE_CHAR_OPERATORS = {OP_POWER, OP_FLOOR_DIV}

# Скобки
OPENING_BRACKET = '('
CLOSING_BRACKET = ')'
BRACKETS = '()'

# Специальные символы
POINT = '.'
UNARY_PLUS_SYMBOL = '$'
UNARY_MINUS_SYMBOL = '~'

# Команды интерфейса
COMMAND_EXIT = 'exit'
COMMAND_HELP = 'help'

# Промпт
PROMPT = '\nRPN> '

# Сообщения об ошибках
ERROR_EMPTY_EXPRESSION = 'Пустое выражение'
ERROR_UNBALANCED_BRACKETS = 'Несбалансированные скобки'
ERROR_NO_TOKENS = 'Выражение не содержит токенов'
ERROR_INVALID_NUMBER = 'Некорректное число: {}'
ERROR_UNKNOWN_SYMBOL = 'Неизвестный символ: {}'
ERROR_DIVISION_BY_ZERO = 'Деление на ноль'
ERROR_EMPTY_BRACKETS = 'Пустые скобки'
ERROR_INVALID_BRACKET_EXPRESSION = 'Некорректное выражение в скобках: осталось {} элементов вместо 1'
ERROR_NOT_ENOUGH_UNARY_ARGS = 'Недостаточно аргументов для унарного оператора'
ERROR_NOT_ENOUGH_BINARY_ARGS = 'Недостаточно аргументов для бинарного оператора'
ERROR_UNKNOWN_OPERATOR = 'Неизвестный оператор: {}'
ERROR_UNKNOWN_UNARY_OPERATOR = 'Неизвестный унарный оператор: {}'
ERROR_INTEGER_ONLY_FLOOR_DIV = 'Операция // только для целых чисел'
ERROR_INTEGER_ONLY_MOD = 'Операция % только для целых чисел'
ERROR_INVALID_EXPRESSION = 'Некорректное выражение: осталось {} элементов в стеке'
ERROR_UNPROCESSED_TOKENS = 'Остались необработанные токены'

# Текст справки
HELP_TEXT = """
RPN Калькулятор
Операции: +, -, *, /, //, %, **
Унарные: ~ (минус), $ (плюс)
Примеры: 3 4 +, 5 ~, 2 ( 3 4 + ) *
Команды: help, exit
"""

# Форматирование вывода
FLOAT_FORMAT = '{:.6g}'
