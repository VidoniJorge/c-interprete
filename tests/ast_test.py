from unittest import TestCase

from lpp.ast import (
    ExpressionStatement,
    Identifier,
    Integer,
    Program,
    LetStatement,
    ReturnStatement
)

from lpp.token import(
    Token,
    TokenType
)

class ASTTest(TestCase):

    def test_let_statements(self) -> None:
        
        program: Program = Program(statements=[
                LetStatement(
                    token = Token(TokenType.LET, literal='variable', line=1), 
                    name  = Identifier(token = Token(TokenType.IDENT, literal = 'mi_var', line=1), value = 'mi_var' ),
                    value = Identifier(token = Token(TokenType.IDENT, literal = 'otra_variable', line=1), value = 'otra_var')
                )
            ]
        )

        program_str = str(program)
        print(program_str)
        self.assertEquals(program_str, 'variable mi_var = otra_var;')
    
    def test_return_statement(self) -> None:
        program: Program = Program(
            statements=[
                ReturnStatement(
                    token = Token(TokenType.RETURN, literal='regresa', line=1),
                    return_value = Identifier(
                                Token(TokenType.IDENT, literal = 'otra_variable',line=1), 
                                value = '5'
                            )
                )
            ]
        )

        program_str = str(program)
        self.assertEquals(program_str, 'regresa 5;')

    def test_integer_expressions(self) -> None:
        program: Program = Program(
            statements=[
                ExpressionStatement(
                    token = Token(TokenType.INT, literal='5', line=1),
                    expression = Integer(
                                Token(TokenType.INT, literal='5', line=1), 
                                value = 5
                            )
                )
            ]
        )

        program_str = str(program)
        print(program_str)
        self.assertEquals(program_str, '5')