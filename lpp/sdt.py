from abc import(
    ABC,
    abstractclassmethod,
)

from lpp.token import Token

class ASTNode(ABC):

    @abstractclassmethod 
    def token_literan(self) -> str:
        pass

    @abstractclassmethod
    def __str__(self) -> str:
        pass

class Statement(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literan(self) -> str:
        return self.token.literal

class Expresiones(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literan(self) -> str:
        return self.token.literal