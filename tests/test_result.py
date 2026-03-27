import pytest
from pyresult import Ok, Err


def test_ok_state():
    res = Ok(10)
    assert res.is_ok() is True
    assert res.is_err() is False


def test_err_state():
    res = Err("Error message")
    assert res.is_ok() is False
    assert res.is_err() is True


def test_unwrap():
    assert Ok("success").unwrap() == "success"

    with pytest.raises(
        RuntimeError, match=r"Call to \`\.unwrap\(\)\` on Err variant: fail"
    ):
        Err("fail").unwrap()


def test_unwrap_err():
    assert Err("fail").unwrap_err() == "fail"

    with pytest.raises(
        RuntimeError, match=r"Call to \`\.unwrap_err\(\)\` on Ok variant: success"
    ):
        Ok("success").unwrap_err()


def test_unwrap_or():
    assert Ok(5).unwrap_or(10) == 5
    assert Err("fail").unwrap_or(10) == 10


def test_unwrap_or_else():
    assert Ok(4).unwrap_or_else(lambda e: len(e)) == 4
    assert Err("fail").unwrap_or_else(lambda e: len(e)) == 4


def test_expect():
    assert Ok(42).expect("Must be a number") == 42

    with pytest.raises(RuntimeError, match="panic: fail"):
        Err("fail").expect("panic")


def test_map():
    assert Ok(5).map(lambda x: x * 2) == Ok(10)
    assert Err("error").map(lambda x: x * 2) == Err("error")


def test_map_err():
    assert Ok(5).map_err(lambda e: f"Log: {e}") == Ok(5)
    assert Err("error").map_err(lambda e: f"Log: {e}") == Err("Log: error")


def test_map_or():
    assert Ok("hello").map_or(0, lambda s: len(s)) == 5
    assert Err("error").map_or(0, lambda s: len(s)) == 0


def test_map_or_else():
    assert Ok("hello").map_or_else(lambda _: 1, lambda s: len(s)) == 5
    assert Err("error").map_or_else(lambda _: 0, lambda s: 1 + len(s)) == 0


def test_and_then():
    def divide_by_two(x: int):
        return Ok(x // 2) if x % 2 == 0 else Err("odd")

    assert Ok(4).and_then(divide_by_two) == Ok(2)
    assert Ok(3).and_then(divide_by_two) == Err("odd")
    assert Err("prev").and_then(divide_by_two) == Err("prev")


def test_or_else():
    def recover(e: str):
        return Ok(0) if e == "recoverable" else Err("fatal")

    assert Ok(5).or_else(recover) == Ok(5)
    assert Err("recoverable").or_else(recover) == Ok(0)
    assert Err("not recoverable").or_else(recover) == Err("fatal")


def test_inspect():
    modified = False

    def side_effect(val):
        nonlocal modified
        modified = True

    Ok(1).inspect(side_effect)
    assert modified is True

    modified = False
    Err("error").inspect(side_effect)
    assert modified is False


def test_inspect_err():
    modified = False

    def side_effect(val):
        nonlocal modified
        modified = True

    Ok(1).inspect_err(side_effect)
    assert modified is False

    Err("error").inspect_err(side_effect)
    assert modified is True
