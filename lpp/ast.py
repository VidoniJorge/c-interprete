from abc import(
    ABC,
    abstractclassmethod,
)

from typing import List

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
    
class Program(ASTNode):

    def __init__(self, statements: List[Statement]) -> None:
        self.statements = statements

    def token_literan(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literan()
        
        return ''

    def __str__(self) -> str:
        out: List[str] = []
        
        for statement in self.statements:
            out.append(str(statement))
        
        return ''.join(out)
