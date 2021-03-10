from unittest import TestCase
from typing import (
    cast,
    List,
    Any
)

from lpp.ast import (
    Expression,
    Identifier,
    Integer,
    Program,
    LetStatement,
    ReturnStatement,
    ExpressionStatement
)
from lpp.lexer import Lexer
from lpp.parser import Parser

class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = 'variable x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)
    
    def test_let_statements(self) -> None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        for statement in program.statements:
            self.assertEqual(statement.token_literan(), 'variable')
            self.assertIsInstance(statement, LetStatement)
        

    def test_names_in_let_statements(self) -> None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        names: List[str] = []
        for statement in program.statements:
            statement = cast(LetStatement, statement)
            assert statement.name is not None
            names.append(statement.name.value)

        expected_names: List[str] = ['x', 'y', 'foo']
        self.assertEquals(names, expected_names)

    def test_parse_error(self) -> None:
        source: str = 'variable x 5'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(parser.errors), 1)
    
    def test_return_statement(self) -> None:
        source: stc = '''
            regresa 5;
            regresa foo;
        '''

        lexer: Lexer = Lexer(source)
        parcer: Parser = Parser(lexer)

        program: Program = parcer.parse_program()

        self.assertEquals(len(program.statements),2)

        for statement in program.statements:
            self.assertEquals(statement.token_literan(), 'regresa')
            self.assertIsInstance(statement, ReturnStatement)

    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statement(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])
        self._test_literal_expression(expression_statement.expression, 'foobar')

    def test_integer_expressions(self) -> None:
        source = str = '5';
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()
        #si hay un error en el parser este test no va a decir que hay un error
        self._test_program_statement(parser, program)
        
        exprassion_statement = cast(ExpressionStatement, program.statements[0])

        assert exprassion_statement.expression is not None
        self._test_literal_expression(exprassion_statement.expression, 5) 

    def _test_program_statement(self,
                                parser: Parser,
                                program: Program,
                                expedted_statement_count: int = 1) -> None:
        self.assertEquals(len(parser.errors), 0)
        self.assertEquals(len(program.statements),expedted_statement_count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)
    
    def _test_literal_expression(self,
                                expression: Expression,
                                expected_value: Any) -> None:
        value_type: Type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)
        elif value_type == int:
            self._test_integer(expression, expected_value)
        else:
            self.fail(f'Unhandled type of expression. Got={value_type}')
    
    def _test_identifier(self,
                        expression: Expression,
                        expected_value: str) -> None:
        
        self.assertIsInstance(expression,Identifier)

        identifier = cast(Identifier, expression)
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)
    
    def _test_integer(  self,
                        expression: Expression,
                        expected_value: int) -> None:
        self.assertIsInstance(expression,Integer)

        integer = cast(Integer, expression)
        self.assertEquals(integer.value, expected_value)
        self.assertEquals(integer.token.literal, str(expected_value))