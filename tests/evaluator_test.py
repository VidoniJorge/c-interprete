from typing import(
    cast,
    List,
    Tuple,
)

from unittest import TestCase

from lpp.ast import Program
from lpp.evaluator import evaluate
from lpp.lexer import Lexer
from lpp.object import (
    Boolean,
    Integer,
    Object
)
from lpp.parser import Parser

class EvaluatorTest(TestCase):

    def test_bang_operator(self) -> None:
        tests: List[Tuple[str:bool]] = [
            ('!verdadero',False),
            ('!falso',True),
            ('!!verdadero',True),
            ('!!falso',False),
            ('!5',False),
            ('!!5',True),
        ]
    
        for source, expected in tests:
            evaluated = self._evaluate_test(source)
            self._test_boolean_object(evaluated, expected)

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str,bool]] = [
            ('verdadero',True),
            ('falso',False),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_test(source)
            self._test_boolean_object(evaluated, expected)


    def test_integer_evaluator(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5',5),
            ('10',10),
            ('-5',-5),
            ('-10',-10),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_test(source)
            self._test_integer_object(evaluated, expected)

    def _evaluate_test(self, source:str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        evaluated = evaluate(program)

        assert evaluated is not None
        return evaluated

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        assert evaluated is not None
        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)


    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)
















