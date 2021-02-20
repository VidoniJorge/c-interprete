from enum import(
    auto, #que automaticamente me genere un valor
    Enum,
    unique #Me permite definir que los enum sean unicos
)

from typing import (
    Dict,
    NamedTuple,
)

@unique
class TokenType(Enum):
    ASSIGN = auto()
    COMMA = auto()
    EOF = auto()
    FUNCTION = auto()
    IDENT = auto()
    ILLEGAL = auto()
    INT = auto()
    LBRANCE = auto()
    LET = auto()
    LPAREN = auto()
    PLUS = auto()
    RBRACE = auto()
    RPAREN = auto()
    SEMICOLON = auto()

class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'

def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'procedimiento': TokenType.FUNCTION,
        'variable': TokenType.LET
    }

    return keywords.get(literal, TokenType.IDENT)