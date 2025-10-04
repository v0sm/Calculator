import pytest
from src.calculator import Calculator


def test_simple():
    """Тестирует базовые арифметические операции."""
    assert Calculator('3 4 2 * +').eval() == 11
    assert Calculator('10 5 2 + *').eval() == 70


def test_parentheses():
    """Тестирует обработку скобок в RPN выражениях."""
    assert Calculator('( 3 4 2 * + )').eval() == 11
    assert Calculator('2 ( 3 4 + ) *').eval() == 14


def test_unary_operators():
    """Тестирует унарные операторы ~ и $."""
    assert Calculator('5 ~').eval() == -5
    assert Calculator('5 $ ~').eval() == -5
    assert Calculator('3 4 + ~').eval() == -7
    assert Calculator('( 2 3 + ~ )').eval() == -5


def test_mixed_unary_binary():
    """Тестирует смешанные операции с вещественными числами."""
    assert Calculator('1 2 3 4 - - - $').eval() == -2
    assert Calculator('10 5 ~ +').eval() == 5


def test_float_operations():
    assert Calculator('2 3 /').eval() == pytest.approx(2/3, rel=1e-8)


def test_errors():
    """Тестирует различные ошибочные ситуации."""
    with pytest.raises(ValueError):
        Calculator('( )').eval()

    with pytest.raises(ValueError):
        Calculator('4 + 3').eval()

    with pytest.raises(ZeroDivisionError):
        Calculator('5 0 /').eval()

    with pytest.raises(ValueError):
        Calculator('~').eval()
