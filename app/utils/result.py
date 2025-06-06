from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")

class Success(Generic[T]):
    def __init__(self, value: T):
        self.value = value
    @property
    def is_success(self) -> bool:
        return True
    @property
    def is_failure(self) -> bool:
        return False
    def unwrap(self) -> T:
        return self.value

class Failure(Generic[E]):
    def __init__(self, error: E):
        self.error = error
    @property
    def is_success(self) -> bool:
        return False
    @property
    def is_failure(self) -> bool:
        return True
    def failure(self) -> E:
        return self.error

Result = Union[Success[T], Failure[E]]
