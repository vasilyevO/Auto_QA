import pytest
from simple_math import SimpleMath

@pytest.fixture
def calculator():
    return SimpleMath()

def test_square(calculator):
    assert calculator.square(2) == 4
    assert calculator.square(-3) == 9
    assert calculator.square(0) == 0

def test_cube(calculator):
    assert calculator.cube(2) == 8
    assert calculator.cube(-3) == -27
    assert calculator.cube(0) == 0