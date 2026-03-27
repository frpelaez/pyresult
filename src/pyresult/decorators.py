from functools import wraps
from typing import Any, Callable

from pyresult import Err, Ok, Result


def safe(*exceptions: type[Exception]):
    catch_exceptions = exceptions if exceptions else (Exception)

    def decorator[T](func: Callable[[Any], T]) -> Callable[[Any], Result[T, Exception]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Result[T, Exception]:
            try:
                return Ok(func(*args, **kwargs))
            except catch_exceptions as e:
                return Err(e)

        return wrapper

    return decorator
