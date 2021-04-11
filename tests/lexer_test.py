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
            Token(TokenType.ILLEGAL, '¡',1),
            Token(TokenType.ILLEGAL, '¿',1),
            Token(TokenType.ILLEGAL, '@',1),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_one_character_operator(self) -> None:
        source: str = '=+-/*<>!'
        
        tokens = self._load_tokens(source)

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '=',1),
            Token(TokenType.PLUS, '+',1),
            Token(TokenType.MINUS, "-",1),
            Token(TokenType.DIVISION, "/",1),
            Token(TokenType.MULTIPLICATION, "*",1),
            Token(TokenType.LT, "<",1),
            Token(TokenType.GT, ">",1),
            Token(TokenType.NEGATION, "!",1)
        ]

        self.assertEqual(tokens, expected_tokens)
    
    def test_two_characters_operator(self) -> None:
        source: str = '''
            10 == 10;
            12 != 11;
        '''
        tokens: List[Token] = self._load_n_tokens(source, 8)
        
        expected_tokens: List[Token] = [
            Token(TokenType.INT, '10',2),
            Token(TokenType.EQ, '==',2),
            Token(TokenType.INT, "10",2),
            Token(TokenType.SEMICOLON, ";",2),
            Token(TokenType.INT, "12",3),
            Token(TokenType.NOT_EQ, "!=",3),
            Token(TokenType.INT, "11",3),
            Token(TokenType.SEMICOLON, ";",3)
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        
        tokens = self._load_n_tokens(source, len(source) + 1  )
        
        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+',1),
            Token(TokenType.EOF, '',1),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_delimeters(self) -> None:
        source = '(){},;'

        tokens = self._load_tokens(source)

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, '(',1),
            Token(TokenType.RPAREN, ')',1),
            Token(TokenType.LBRACE, '{',1),
            Token(TokenType.RBRACE, '}',1),
            Token(TokenType.COMMA, ',',1),
            Token(TokenType.SEMICOLON, ';',1),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_assignment(self) -> None:
        source = 'variable cinco = 5 ;'

        tokens: List[Token] = self._load_n_tokens(source,5)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable',1),
            Token(TokenType.IDENT, 'cinco',1),
            Token(TokenType.ASSIGN, '=',1),
            Token(TokenType.INT, '5',1),
            Token(TokenType.SEMICOLON, ';',1),
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
            Token(TokenType.LET, 'variable',2),
            Token(TokenType.IDENT, 'suma',2),
            Token(TokenType.ASSIGN, '=',2),
            Token(TokenType.FUNCTION, 'procedimiento',2),
            Token(TokenType.LPAREN, '(',2),
            Token(TokenType.IDENT, 'x',2),
            Token(TokenType.COMMA, ',',2),
            Token(TokenType.IDENT, 'y',2),
            Token(TokenType.RPAREN, ')',2),
            Token(TokenType.LBRACE, '{',2),
            Token(TokenType.IDENT, 'x',3),
            Token(TokenType.PLUS, '+',3),
            Token(TokenType.IDENT, 'y',3),
            Token(TokenType.SEMICOLON, ';',3),
            Token(TokenType.RBRACE, '}',4),
            Token(TokenType.SEMICOLON, ';',4),
        ]
        
        self.assertEqual(tokens, expected_tokens)


    def test_function_call(self) -> None:
        source: str = 'variable resultado = suma(dos, tres);'

        tokens: List[Token] = self._load_n_tokens(source,10)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable',1),
            Token(TokenType.IDENT, 'resultado',1),
            Token(TokenType.ASSIGN, '=',1),
            Token(TokenType.IDENT, 'suma',1),
            Token(TokenType.LPAREN, '(',1),
            Token(TokenType.IDENT, 'dos',1),
            Token(TokenType.COMMA, ',',1),
            Token(TokenType.IDENT, 'tres',1),
            Token(TokenType.RPAREN, ')',1),
            Token(TokenType.SEMICOLON, ';',1),
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
            Token(TokenType.IF, 'si',2),
            Token(TokenType.LPAREN, '(',2),
            Token(TokenType.INT, '5',2),
            Token(TokenType.LT, '<',2),
            Token(TokenType.INT, '10',2),
            Token(TokenType.RPAREN, ')',2),
            Token(TokenType.LBRACE, '{',2),
            Token(TokenType.RETURN, 'regresa',3),
            Token(TokenType.TRUE, 'verdadero',3),
            Token(TokenType.SEMICOLON, ';',3),
            Token(TokenType.RBRACE, '}',4),
            Token(TokenType.ELSE, 'si_no',4),
            Token(TokenType.LBRACE, '{',4),
            Token(TokenType.RETURN, 'regresa',5),
            Token(TokenType.FALSE, 'falso',5),
            Token(TokenType.SEMICOLON, ';',5),
            Token(TokenType.RBRACE, '}',6),
        ]

        self.assertEqual(tokens, expected_tokens)
    
    def test_variable_witch_number(self) -> None:
        source: str = 'variable valor_1;'
        tokens: List[TokenType] = self._load_n_tokens(source,3)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable',1),
            Token(TokenType.IDENT, 'valor_1',1),
            Token(TokenType.SEMICOLON, ';',1),
        ]
        print(tokens)
        self.assertEqual(tokens, expected_tokens)
    
    def test_string(self) -> None:
        source: str = '''
            "foo";
            "No hay mejor escuela que la que uno se genera";
        '''

        tokens = self._load_n_tokens(source,4)

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, 'foo',2),
            Token(TokenType.SEMICOLON, ';',2),
            Token(TokenType.STRING, 'No hay mejor escuela que la que uno se genera',3),
            Token(TokenType.SEMICOLON, ';',3)
        ]

        self.assertEquals(tokens, expected_tokens)

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
