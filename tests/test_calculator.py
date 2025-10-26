"""Тесты для калькулятора."""
import pytest
from calculator import Calculator


def test_simple_addition():
    """Тестирует простое сложение."""
    assert Calculator('3 4 +').eval() == 7
    assert Calculator('10 5 +').eval() == 15


def test_simple_subtraction():
    """Тестирует простое вычитание."""
    assert Calculator('10 3 -').eval() == 7
    assert Calculator('5 8 -').eval() == -3


def test_simple_multiplication():
    """Тестирует простое умножение."""
    assert Calculator('3 4 *').eval() == 12
    assert Calculator('7 6 *').eval() == 42


def test_simple_division():
    """Тестирует простое деление."""
    assert Calculator('20 4 /').eval() == 5
    assert Calculator('7 2 /').eval() == 3.5


def test_power():
    """Тестирует возведение в степень."""
    assert Calculator('2 3 **').eval() == 8
    assert Calculator('5 2 **').eval() == 25
    assert Calculator('10 0 **').eval() == 1


def test_floor_division():
    """Тестирует целочисленное деление."""
    assert Calculator('7 2 //').eval() == 3
    assert Calculator('10 3 //').eval() == 3
    assert Calculator('5.0 2.0 //').eval() == 2


def test_modulo():
    """Тестирует остаток от деления."""
    assert Calculator('7 3 %').eval() == 1
    assert Calculator('10 4 %').eval() == 2
    assert Calculator('5.0 2.0 %').eval() == 1


def test_complex_expressions():
    """Тестирует сложные выражения."""
    assert Calculator('3 4 2 * +').eval() == 11
    assert Calculator('10 5 2 + *').eval() == 70
    assert Calculator('15 7 1 1 + - / 3 * 2 1 1 + + -').eval() == 5


def test_parentheses():
    """Тестирует обработку скобок в RPN выражениях."""
    assert Calculator('( 3 4 2 * + )').eval() == 11
    assert Calculator('2 ( 3 4 + ) *').eval() == 14
    assert Calculator('( 2 3 + ) ( 4 5 + ) *').eval() == 45


def test_nested_parentheses():
    """Тестирует вложенные скобки."""
    assert Calculator('( ( 2 3 + ) 4 * )').eval() == 20
    assert Calculator('( 1 ( 2 3 + ) + )').eval() == 6


def test_unary_minus():
    """Тестирует унарный минус."""
    assert Calculator('5 ~').eval() == -5
    assert Calculator('3 4 + ~').eval() == -7
    assert Calculator('( 2 3 + ~ )').eval() == -5


def test_unary_plus():
    """Тестирует унарный плюс."""
    assert Calculator('5 $').eval() == 5
    assert Calculator('5 $ ~').eval() == -5


def test_mixed_unary_binary():
    """Тестирует смешанные операции."""
    assert Calculator('1 2 3 4 - - - $').eval() == -2
    assert Calculator('10 5 ~ +').eval() == 5
    assert Calculator('3 ~ 4 ~  +').eval() == -7


def test_float_numbers():
    """Тестирует операции с дробными числами."""
    assert Calculator('2.5 2 *').eval() == 5.0
    assert Calculator('3.14 2 +').eval() == pytest.approx(5.14)
    assert Calculator('2 3 /').eval() == pytest.approx(2 / 3, rel=1e-8)
    assert Calculator('10.5 2.5 +').eval() == 13.0


def test_negative_numbers():
    """Тестирует отрицательные числа в выражении."""
    assert Calculator('5~ 3 +').eval() == -2
    assert Calculator('10~ 5~ +').eval() == -15
    assert Calculator('3~ 4 *').eval() == -12


def test_mixed_int_float():
    """Тестирует смешанные целые и дробные числа."""
    assert Calculator('2 3.5 +').eval() == 5.5
    assert Calculator('10 2.5 /').eval() == 4.0


def test_empty_expression():
    """Тестирует пустое выражение."""
    with pytest.raises(ValueError, match="Пустое выражение"):
        Calculator('').eval()

    with pytest.raises(ValueError, match="Пустое выражение"):
        Calculator('   ').eval()


def test_empty_brackets():
    """Тестирует пустые скобки."""
    with pytest.raises(ValueError, match="Пустые скобки"):
        Calculator('( )').eval()


def test_unbalanced_brackets():
    """Тестирует несбалансированные скобки."""
    with pytest.raises(ValueError, match="Несбалансированные скобки"):
        Calculator('( 2 3 +').eval()

    with pytest.raises(ValueError, match="Несбалансированные скобки"):
        Calculator('2 3 + )').eval()

    with pytest.raises(ValueError, match="Несбалансированные скобки"):
        Calculator('( ( 2 3 + )').eval()


def test_invalid_bracket_content():
    """Тестирует некорректное содержимое скобок."""
    with pytest.raises(ValueError, match="Некорректное выражение в скобках"):
        Calculator('( 2 3 )').eval()


def test_division_by_zero():
    """Тестирует деление на ноль."""
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        Calculator('5 0 /').eval()

    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        Calculator('10 0 //').eval()

    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        Calculator('7 0 %').eval()


def test_insufficient_operands_binary():
    """Тестирует недостаточное количество операндов для бинарных операций."""
    with pytest.raises(ValueError, match="Недостаточно аргументов для бинарного оператора"):
        Calculator('5 +').eval()

    with pytest.raises(ValueError, match="Недостаточно аргументов для бинарного оператора"):
        Calculator('+').eval()

    with pytest.raises(ValueError, match="Недостаточно аргументов"):
        Calculator('4 + 3').eval()


def test_insufficient_operands_unary():
    """Тестирует недостаточное количество операндов для унарных операций."""
    with pytest.raises(ValueError, match="Недостаточно аргументов для унарного оператора"):
        Calculator('~').eval()

    with pytest.raises(ValueError, match="Недостаточно аргументов для унарного оператора"):
        Calculator('$').eval()


def test_too_many_operands():
    """Тестирует слишком много операндов (остаются необработанные)."""
    with pytest.raises(ValueError, match="Некорректное выражение"):
        Calculator('2 3 4').eval()

    with pytest.raises(ValueError, match="Некорректное выражение"):
        Calculator('5 6 + 7').eval()


def test_invalid_characters():
    """Тестирует неизвестные символы."""
    with pytest.raises(ValueError, match="Неизвестный символ"):
        Calculator('2 3 @').eval()

    with pytest.raises(ValueError, match="Неизвестный символ"):
        Calculator('2 3 + &').eval()


def test_floor_division_float_error():
    """Тестирует ошибку при использовании // с нецелыми float."""
    with pytest.raises(TypeError, match="Операция // только для целых чисел"):
        Calculator('7.5 2 //').eval()

    with pytest.raises(TypeError, match="Операция // только для целых чисел"):
        Calculator('10 2.3 //').eval()


def test_modulo_float_error():
    """Тестирует ошибку при использовании % с нецелыми float."""
    with pytest.raises(TypeError, match="Операция % только для целых чисел"):
        Calculator('7.5 2 %').eval()

    with pytest.raises(TypeError, match="Операция % только для целых чисел"):
        Calculator('10 2.3 %').eval()


def test_zero_operations():
    """Тестирует операции с нулем."""
    assert Calculator('0 5 +').eval() == 5
    assert Calculator('0 5 *').eval() == 0
    assert Calculator('5 0 -').eval() == 5


def test_negative_results():
    """Тестирует выражения с отрицательными результатами."""
    assert Calculator('3 5 -').eval() == -2
    assert Calculator('0 7 -').eval() == -7


def test_large_numbers():
    """Тестирует операции с большими числами."""
    assert Calculator('1000000 2000000 +').eval() == 3000000
    assert Calculator('999 999 *').eval() == 998001


def test_very_small_numbers():
    """Тестирует операции с очень маленькими числами."""
    assert Calculator('0.001 0.002 +').eval() == pytest.approx(0.003)


def test_expression_with_spaces():
    """Тестирует выражения с различным количеством пробелов."""
    assert Calculator('  3   4   +  ').eval() == 7
    assert Calculator('2    3    *').eval() == 6
