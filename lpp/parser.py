from typing import Optional

from lpp.ast import (
    Identifier,
    LetStatement,
    Program,
    Statement
)
from lpp.lexer import Lexer

from lpp.token import (
    Token,
    TokenType
)
class Parser:

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        
        self._advance_token()
        self._advance_token()

    def parse_program(self) -> Program:
        programa: Program = Program(statements = [])

        assert self._current_token is not None
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parser_statement()
            if statement is not None:
                programa.statements.append(statement)
            
            self._advance_token()

        return programa

    def _advance_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _expected_token(self,token_type: TokenType) -> bool:
        assert self._peek_token is not None
        if self._peek_token.token_type == token_type:
            self._advance_token()
            return True
        return False

    def _parser_let_statement(self) -> Optional[LetStatement]:
        assert self._current_token is not None
        let_statement  = LetStatement(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None

        let_statement.name = Identifier(token=self._current_token, 
                                        value=self._current_token.literal)

        if not self._expected_token(TokenType.ASSIGN) :
            return None
        
        #TODO terminar cuando sepamos parsear expreciones
        while self._current_token.token_type != TokenType.SEMICOLON and self._current_token.token_type != TokenType.EOF:
            self._advance_token()       
        
        return let_statement

    def _parser_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        
        if self._current_token.token_type == TokenType.LET:
            return self._parser_let_statement()
        else:
            return None