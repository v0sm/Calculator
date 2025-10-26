"""Главный модуль калькулятора."""
from tokenizer import Tokenizer
from evaluator import Evaluator


class Calculator:
    """
    RPN калькулятор.

    Координирует работу токенизатора и вычислителя.
    Принимает строковые выражения в RPN формате и вычисляет их значения.
    """

    def __init__(self, expression: str):
        """
        Инициализирует калькулятор.

        Args:
            expression: Выражение в RPN формате.
        """
        self.expression = expression

    def eval(self) -> float:
        """
        Вычисляет значение RPN выражения.

        Returns:
            Числовой результат вычисления выражения.

        Raises:
            ValueError: При некорректном выражении.
        """
        tokenizer = Tokenizer(self.expression)
        tokens = tokenizer.tokenize()

        evaluator = Evaluator(tokens)
        result = evaluator.evaluate()

        return result
