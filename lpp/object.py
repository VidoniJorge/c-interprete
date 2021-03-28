from abc import (
    ABC,
    abstractclassmethod,
)

from enum import(
    auto,
    Enum,
)

class ObjectType(Enum):
    BOOLEAN = auto()
    INTEGER = auto()
    NULL = auto()

class Object(ABC):

    @abstractclassmethod
    def type(self) -> ObjectType:
        pass

    @abstractclassmethod
    def inspect(self) -> str:
        pass

class Integer(Object):

    def __init__(self, value: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)

class Boolean(Object):

    def __init__(self, value: bool) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return 'verdadero' if self.value else 'falso'

class Null(Object):

    def type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return 'null'