# pyresult 

Bring Rust's elegant and predictable error handling to Python. 

`pyresult` provides a robust `Result[T, E]` type for Python 3.12+, allowing you to handle operations that can fail without relying on unexpected `try/except` blocks or hidden control flow jumps.

## Features

- **Rust-like API**: Implements familiar methods like `unwrap`, `map`, `and_then`, `or_else`, and `inspect`.
- **Modern Python typing**: Built from the ground up utilizing Python 3.12+ generic syntax (`PEP 695`) for flawless static typing and IDE auto-completion.
- **Pattern matching ready**: Fully compatible with Python 3.10+ `match/case` structural pattern matching.
- **The `@safe` recorator**: Easily bridge standard Python exceptions into the `Result` paradigm.

## Installation

You can install `pyresult` directly from github using modern package managers like `uv` (recommended) or `pip`:

```bash
# Using uv
uv add git+https://github.com/frpelaez/pyresult.git

# Using pip
pip install git+https://github.com/frpelaez/pyresult.git
```

## Usage guide

### 1. Basic error handling (`Ok` and `Err`)

Instead of raising exceptions, return an `Ok` containing the successful value, or an `Err` containing the error context.

```python
from pyresult import Result, Ok, Err

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero is not allowed.")
    return Ok(a / b)

# Unpacking the result
res = divide(10, 2)
if res.is_ok():
    print(f"Success: {res.unwrap()}")  # Output: Success: 5.0
```

### 2. Pattern matching

`pyresult` shines when combined with Python's structural pattern matching, enforcing clean and readable error handling.

```python
from pyresult import Ok, Err

def process_data(data: str):
    match divide(int(data), 2):
        case Ok(value):
            print(f"The calculated value is {value}")
        case Err(error):
            print(f"Failed to process: {error}")
```

### 3. Method chaining

Avoid nested `if/else` statements by chaining operations. Methods like `and_then` (for operations that return a `Result`) and `map` (for standard transformations) make pipelines incredibly clean.

```python
from pyresult import Result, Ok, Err

def parse_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err(f"Cannot parse '{s}'")

# Pipeline: Parse -> Divide -> Format string
result = (
    parse_int("20")
    .and_then(lambda x: divide(x, 2))
    .map(lambda x: f"Final result: {x}")
    .unwrap_or("Fallback value")
)

print(result) # Output: Final result: 10.0
```

### 4. The `@safe` decorator

Interacting with third-party libraries or the standard library often involves exceptions. The `@safe` decorator automatically catches exceptions and wraps the output in a `Result`.

```python
import json
from pyresult import safe, Ok, Err

# Catch specific exceptions
@safe(json.JSONDecodeError)
def parse_json(payload: str) -> dict:
    return json.loads(payload)

# If it fails, it returns an Err(JSONDecodeError) instead of crashing
match parse_json('{"name": "Python"}'):
    case Ok(data):
        print(f"Parsed: {data['name']}")
    case Err(e):
        print(f"Invalid JSON: {e}")

# If you don't provide arguments to @safe(), it catches Exception by default.
```

## Requirements

- Python >= 3.12
