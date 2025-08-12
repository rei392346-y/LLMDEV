import pytest

# bが0の場合、ValueErrorを発生させる除算関数
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# 0で除算したときにValueErrorが発生するかをテスト
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# 通常の除算が正しく行われるかをテスト
def test_divide_normal():
    result = divide(10, 2)
    assert result == 5