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
    ERROR = auto()
    INTEGER = auto()
    NULL = auto()
    RETURN = auto()

class Object(ABC):

    @abstractclassmethod
    def type(self) -> ObjectType:
        pass

    @abstractclassmethod
    def inspect(self) -> str:
        pass

class Boolean(Object):

    def __init__(self, value: bool) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return 'verdadero' if self.value else 'falso'

class Error(Object):

    def __init__(self, message) -> None:
        self.message = message
    
    def type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f'Error: {self.message}'

class Integer(Object):

    def __init__(self, value: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)

class Null(Object):

    def type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return 'null'

class Return(Object):

    def __init__(self, value: Object) -> None:
        self.value = value
    
    def type(self) -> ObjectType:
        return ObjectType.RETURN
    
    def inspect(self) -> str:
        return self.value.inspect()
