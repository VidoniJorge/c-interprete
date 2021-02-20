from unittest import TestCase
from typing import List

from lpp.token import(
    Token,
    TokenType
)

from lpp.lexer import Lexer

class LexerTest(TestCase):

    def test_illegal(self) -> None:
        source: str = '¡¿@'
        lexer: Lexer = Lexer(source)

        tokens = self._load_tokens(source)

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),
            Token(TokenType.ILLEGAL, '@'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_one_character_operator(self) -> None:
        source: str = '=+-/*<>!'
        
        tokens = self._load_tokens(source)

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIVISION, "/"),
            Token(TokenType.MULTIPLICATION, "*"),
            Token(TokenType.LT, "<"),
            Token(TokenType.GT, ">"),
            Token(TokenType.NEGATION, "!")
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        
        tokens = self._load_n_tokens(source, len(source) + 1  )
        
        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_delimeters(self) -> None:
        source = '(){},;'

        tokens = self._load_tokens(source)

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRANCE, '{'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_assignment(self) -> None:
        source = 'variable cinco = 5 ;'

        tokens: List[Token] = self._load_n_tokens(source,5)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'cinco'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)
        

    def test_function_declaration(self) -> None:
        source: str = '''
            variable suma = procedimiento(x, y) {
                x + y;
            }; 
        '''

        tokens: List[Token] = self._load_n_tokens(source,16)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.FUNCTION, 'procedimiento'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRANCE, '{'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        
        self.assertEqual(tokens, expected_tokens)


    def test_function_call(self) -> None:
        source: str = 'variable resultado = suma(dos, tres);'

        tokens: List[Token] = self._load_n_tokens(source,10)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'resultado'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'dos'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'tres'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_control_statement(self) -> None:
        source: str = '''
            si ( 5 < 10 ){
                regresa verdadero;
            } si_no {
                regresa falso;
            }
        '''

        tokens: List[Token] = self._load_n_tokens(source,17)

        expected_tokens: List[Token] = [
            Token(TokenType.IF, 'si'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.INT, '5'),
            Token(TokenType.LT, '<'),
            Token(TokenType.INT, '10'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRANCE, '{'),
            Token(TokenType.RETURN, 'regresa'),
            Token(TokenType.TRUE, 'verdadero'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.ELSE, 'si_no'),
            Token(TokenType.LBRANCE, '{'),
            Token(TokenType.RETURN, 'regresa'),
            Token(TokenType.FALSE, 'falso'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def _load_tokens(self, source: str) -> List[Token]:
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())
        
        return tokens

    def _load_n_tokens(self, source: str, size: int) -> List[Token]:
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(size):
            tokens.append(lexer.next_token())
        
        return tokens
