import readline

from typing import List

from os import system, name

from lpp.ast import Program
from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.token import (
    Token,
    TokenType
)

EOF_TOKEN: Token = Token(TokenType.EOF, '')

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
    space: str='  '
    print(space * amount_space + statement)    

def start_repl() -> None:
    while  (source := input('>> ')) != 'salir()':
        if source == "limpiar()":
            clear()
        else:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)
            
            program: Program = parser.parse_program()

            if len(parser.errors) > 0:
                _print_parse_erros(parser.errors)
                continue
            
            print(program)

            str_program: str = program.__str__()
            statement: str = ''
            count_paremt = 0
            for i, caracter in enumerate(str_program):
                if caracter == '(':
                    _print_statement(caracter,count_paremt)
                    count_paremt +=1
                elif caracter == ')':
                    if statement != '':
                        _print_statement(statement,count_paremt)
                    count_paremt -=1
                    _print_statement(caracter,count_paremt)
                    statement = ''
                elif caracter == ';':
                    statement += caracter
                    if statement != '':
                        _print_statement(statement,count_paremt)
                    statement = ''
                else:
                    if not (statement == '' and caracter == ' '):
                        statement += caracter
                
            _print_statement(statement,count_paremt)
            


                
            
        