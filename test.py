import pytest
from src.calculator import Calculator


def test_simple():
    assert Calculator('3 4 2 * +').eval() == 11
    assert Calculator('10 5 2 + *').eval() == 70


def test_parentheses():
    assert Calculator('( 3 4 2 * + )').eval() == 11
    assert Calculator('2 ( 3 4 + ) *').eval() == 14


def test_unary_operators():
    assert Calculator('5 ~').eval() == -5
    assert Calculator('5 $ ~').eval() == -5
    assert Calculator('3 4 + ~').eval() == -7
    assert Calculator('( 2 3 + ~ )').eval() == -5


def test_mixed_unary_binary():
    assert Calculator('1 2 3 4 - - - $').eval() == -2
    assert Calculator('10 5 ~ +').eval() == 5


def test_float_operations():
    result = Calculator('2 3 /').eval()
    assert abs(result - 2 / 3) < 1e-8


def test_errors():
    with pytest.raises(ValueError):
        Calculator('( )').eval()

    with pytest.raises(ValueError):
        Calculator('4 + 3').eval()

    with pytest.raises(ZeroDivisionError):
        Calculator('5 0 /').eval()

    with pytest.raises(ValueError):
        Calculator('~').eval()
