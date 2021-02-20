from re import match

from lpp.token import(
    lookup_token_type,
    Token,
    TokenType
)

class Lexer:
    
    #Constructor
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ''
        self._read_position: int = 0
        self._position: int = 0

        self._read_caracter()

    def next_token(self) -> Token:
        token = self._character_to_token()
        return token

    def _character_to_token(self) -> Token:
        self._skip_whitespace()
        if match(r'^=$', self._character):
            token = Token(TokenType.ASSIGN, self._character)
        elif match(r'^\+$', self._character):
            token = Token(TokenType.PLUS, self._character)
        elif match(r'^$', self._character):
            token = Token(TokenType.EOF, self._character)
        elif match(r'^\($', self._character):
            token = Token(TokenType.LPAREN, self._character)
        elif match(r'^\)$', self._character):
            token = Token(TokenType.RPAREN, self._character)
        elif match(r'^\{$', self._character):
            token = Token(TokenType.LBRANCE, self._character)
        elif match(r'^}$', self._character):
            token = Token(TokenType.RBRACE, self._character)
        elif match(r'^,$', self._character):
            token = Token(TokenType.COMMA, self._character)
        elif match(r'^;$', self._character):
            token = Token(TokenType.SEMICOLON, self._character)
        elif self._is_letter(self._character):
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)
            #TODO ver si podemos volver al codigo donde no se hacia el return, 
            # se cambio por el problema el _read_caracter donde no pasaba la prueba 
            # test_function_declaration por no tener espacios en blanco entre la declaracion
            # del procedimiento y el ()
            return Token(token_type, literal)
        elif self._is_number_(self._character):
            literal = self._read_number()
            return Token(TokenType.INT, literal)
        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_caracter()
        return token

    def _read_caracter(self):
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]
        
        self._position = self._read_position
        self._read_position += 1

    def _read_identifier(self) -> str:
        initial_position = self._position
        while self._is_letter(self._character) :
            self._read_caracter()
        
        return self._source[initial_position:self._position]

    # Es una letra valida
    def _is_letter(self, character) -> bool:
        return bool(match(r'[a-zàèìòùA-ZÀÈÌÒÙñÑ_]',character))

    
    def _read_number(self) -> str:
        initial_position = self._position
        while self._is_number_(self._character) :
            self._read_caracter()
        
        return self._source[initial_position:self._position]

    # Es un numero
    def _is_number_(self, character: str) -> bool:
        return bool(match(r'^\d$',character))
    
    #Ignora el espacio en blanck
    def _skip_whitespace(self) -> str:
        while match(r'^\s$',self._character):
            self._read_caracter()


    