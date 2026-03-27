import json

from pyresult import Err, Ok, Result, safe


def parse_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err(f"Unnable to parse '{s}' as an integer")


def divide_by_two(num: int) -> Result[int, str]:
    return Ok(num // 2)


@safe(json.JSONDecodeError)
def parse_json(data: str) -> dict:
    return json.loads(data)


def main():
    res_success = (
        parse_int("10").and_then(divide_by_two).map(lambda x: f"The result is {x}")
    )
    print(res_success)

    res_fail = (
        parse_int("hello")
        .and_then(divide_by_two)
        .map_err(lambda e: f"Mapped exception from: {e}")
    )
    print(res_fail)

    match parse_json('{"name":"Example"}'):
        case Ok(value):
            print(f"Success: {value['name']}")
        case Err(e):
            print(f"Failed to load json: {e}")

    match parse_json("invalid {json: string}"):
        case Ok(value):
            print(f"Success: {value['name']}")
        case Err(e):
            print(f"Failed to load json: {e}")
