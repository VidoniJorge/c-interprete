from unittest import TestCase
from typing import (
    cast,
    List,
    Any,
    Tuple,
    Type
)

from lpp.ast import (
    Boolean,
    Expression,
    Identifier,
    Infix,
    Integer,
    Prefix,
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

    def test_boolean_expression(self) -> None:
        source: str = 'verdadero; falso;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statement(parser, program, expedted_statement_count=2)

        expected_values: List[bool] = [True,  False]

        for statement, expected_value in zip(program.statements, expected_values):
            expression_statement = cast(ExpressionStatement, statement)

            assert expression_statement is not None
            self._test_literal_expression(expression_statement.expression,
                                            expected_value)

    def test_infix_expression(self) -> None:
        source: str = '''
            5 + 5;
            5 - 5;
            5 * 5;
            5 / 5;
            5 > 5;
            5 < 5;
            5 == 5;
            5 != 5;
        '''

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statement(parser, program, expedted_statement_count=8)

        expected_operators_and_values: List[Tuple[Any, str, Any]] = [
            (5,'+',5),
            (5,'-',5),
            (5,'*',5),
            (5,'/',5),
            (5,'>',5),
            (5,'<',5),
            (5,'==',5),
            (5,'!=',5),
        ]

        for statement, (expected_left, expected_operator, expected_right) in zip(
            program.statements, expected_operators_and_values
        ):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(
                statement.expression,
                expected_left, 
                expected_operator, 
                expected_right
            )

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

    def test_prefix_expression(self) -> None:
        source = '!5; -15;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statement(parser, program, expedted_statement_count=2)

        for statement, (expected_operator, expected_value) in zip(
            program.statements, (['!',5],['-',15])
        ):
            statement = cast(ExpressionStatement, statement)
            self.assertIsInstance(statement.expression, Prefix)
        
            prefix = cast(Prefix, statement.expression)
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right, expected_value)

    def _test_boolean(  self,
                        expression: Expression,
                        expected_value: bool):
        self.assertIsInstance(expression, Boolean)
        boolean = cast(Boolean, expression)

        self.assertEquals(boolean.value, expected_value)
        self.assertEquals(boolean.token.literal, 'verdadero' if expected_value else 'falso')

    def _test_program_statement(self,
                                parser: Parser,
                                program: Program,
                                expedted_statement_count: int = 1) -> None:
        if parser.errors:
            print(parser.errors)

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
        elif value_type == bool:
            self._test_boolean(expression, expected_value)
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
    
    def _test_infix_expression( self,
                                expression: Expression,
                                expected_left: Any,
                                expected_operator: str,
                                expected_right: Any):
        infix = cast(Infix, expression)

        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        self.assertEquals(infix.operator, expected_operator)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)