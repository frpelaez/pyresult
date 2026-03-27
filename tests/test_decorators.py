import pytest
from pyresult import safe


def test_safe_success():
    @safe()
    def divide(a: int, b: int) -> float:
        return a / b

    result = divide(10, 2)

    assert result.is_ok()
    assert result.unwrap() == 5.0


def test_safe_catches_any_exception():
    @safe()
    def divide(a: int, b: int) -> float:
        return a / b

    result = divide(10, 0)

    assert result.is_err()
    assert isinstance(result.unwrap_err(), ZeroDivisionError)


def test_safe_catches_specific_exception():
    @safe(ValueError)
    def parse_int(s: str) -> int:
        return int(s)

    result = parse_int("hello")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), ValueError)


def test_safe_lets_unhandled_exceptions_propagate():
    @safe(ValueError)
    def risky_function(x: int) -> float:
        return 10 / x

    with pytest.raises(ZeroDivisionError):
        risky_function(0)


def test_safe_passes_arguments_correctly():
    @safe()
    def build_string(prefix: str, suffix: str = "") -> str:
        return f"{prefix}_{suffix}"

    result = build_string("hello", suffix="world")

    assert result.unwrap() == "hello_world"
