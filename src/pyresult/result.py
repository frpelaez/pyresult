from dataclasses import dataclass
from typing import Any, Callable


class Result[T, E]:
    def is_ok(self) -> bool:
        raise NotADirectoryError

    def is_err(self) -> bool:
        raise NotADirectoryError

    def unwrap(self) -> T:
        raise NotADirectoryError

    def unwrap_err(self) -> E:
        raise NotImplementedError

    def unwrap_or(self, default: T) -> T:
        raise NotADirectoryError

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        raise NotADirectoryError

    def expect(self, msg: str) -> T:
        raise NotImplementedError

    def expect_err(self, msg: str) -> E:
        raise NotImplementedError

    def map[U](self, f: Callable[[T], U]) -> "Result[U, E]":
        raise NotImplementedError

    def map_err[F](self, f: Callable[[E], F]) -> "Result[T, F]":
        raise NotImplementedError

    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        raise NotImplementedError

    def map_or_else[U](self, default_f: Callable[[E], U], f: Callable[[T], U]) -> U:
        raise NotImplementedError

    def and_then[U](self, f: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        raise NotImplementedError

    def or_else[F](self, f: Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        raise NotImplementedError

    def inspect(self, f: Callable[[T], Any]) -> "Result[T, E]":
        raise NotImplementedError

    def inspect_err(self, f: Callable[[E], Any]) -> "Result[T, E]":
        raise NotImplementedError


@dataclass(frozen=True)
class Ok[T](Result[T, Any]):
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> Any:
        raise RuntimeError(f"Call to `.unwrap_err()` on Ok variant: {self.value}")

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else[T](self, f: Callable[[Any], T]) -> T:
        return self.value

    def expect(self, msg: str) -> T:
        return self.value

    def expect_err(self, msg: str) -> Any:
        raise RuntimeError(f"{msg}: {self.value}")

    def map[U](self, f: Callable[[T], U]) -> "Result[U, Any]":
        return Ok(f(self.value))

    def map_err[U](self, f: Callable[[Any], U]) -> "Result[T, U]":
        return self

    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        return f(self.value)

    def map_or_else[U](self, default_f: Callable[[Any], U], f: Callable[[T], U]) -> U:
        return f(self.value)

    def and_then[U](self, f: Callable[[T], "Result[U, Any]"]) -> "Result[U, Any]":
        return f(self.value)

    def or_else[F](self, f: Callable[[Any], "Result[T, F]"]) -> "Result[T, F]":
        return self

    def inspect(self, f: Callable[[T], Any]) -> "Result[T, Any]":
        f(self.value)
        return self

    def inspect_err(self, f: Callable[[Any], Any]) -> "Result[T, Any]":
        return self


@dataclass(frozen=True)
class Err[E](Result[Any, E]):
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> Any:
        raise RuntimeError(f"Call to `.unwrap()` on Err variant: {self.error}")

    def unwrap_err(self) -> E:
        return self.error

    def unwrap_or[T](self, default: T) -> T:
        return default

    def unwrap_or_else[T](self, f: Callable[[E], T]) -> T:
        return f(self.error)

    def expect(self, msg: str) -> Any:
        raise RuntimeError(f"{msg}: {self.error}")

    def expect_err(self, msg: str) -> E:
        return self.error

    def map[U](self, f: Callable[[Any], U]) -> "Result[U, E]":
        return self

    def map_err[F](self, f: Callable[[E], F]) -> "Result[Any, F]":
        return Err(f(self.error))

    def map_or[U](self, default: U, f: Callable[[Any], U]) -> U:
        return default

    def map_or_else[U](self, default_f: Callable[[E], U], f: Callable[[Any], U]) -> U:
        return default_f(self.error)

    def and_then[U](self, f: Callable[[Any], "Result[U, E]"]) -> "Result[U, E]":
        return self

    def or_else[F](self, f: Callable[[E], F]) -> "Result[Any, F]":
        return f(self.error)

    def inspect(self, f: Callable[[Any], Any]) -> "Result[Any, E]":
        return self

    def inspect_err(self, f: Callable[[E], Any]) -> "Result[Any, E]":
        f(self.error)
        return self
