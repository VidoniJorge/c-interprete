import readline

from typing import List

from os import system, name

from lpp.ast import Program
from lpp.lexer import Lexer
from lpp.object import Environment

from lpp.parser import Parser
from lpp.token import (
    Token,
    TokenType
)
from lpp.evaluator import evaluate

#EOF_TOKEN: Token = Token(TokenType.EOF, '')

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def _print_parse_erros(errors: List[str]):
    for error in errors:
        print(error)

def _print_statement(statement:str, amount_space:int):
    space: str = '  '
    print(space * amount_space + statement)    

def start_repl() -> None:
    scanned: List[str] = []
    while  (source := input('>> ')) != 'salir()':
        if source == "limpiar()":
            clear()
        else:
            scanned.append(source)
            lexer: Lexer = Lexer(' '.join(scanned))
            parser: Parser = Parser(lexer)
            
            program: Program = parser.parse_program()

            if len(parser.errors) > 0:
                _print_parse_erros(parser.errors)
                continue
            
            env: Environment = Environment()
            evaluated = evaluate(program, env)
            if evaluated is not None:
                print(evaluated.inspect())


                
            
        