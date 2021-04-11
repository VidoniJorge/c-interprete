from re import match

from lpp.token import(
    lookup_token_type,
    Token,
    TokenType
)

class Lexer:
    
    #Constructor
    def __init__(self, source: str) -> None:
        self._current_line = 1
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
        #if match(r'^=$', self._character):
        if self._is_token('='):
            if self.sefl_peek_character() == '=':
                token = self._make_two_character_token(TokenType.EQ)
            else:
                token = Token(TokenType.ASSIGN, self._character, self._current_line)
        elif self._is_token('\+'):
            token = Token(TokenType.PLUS, self._character, self._current_line)
        elif self._is_token('\-'):
            token = Token(TokenType.MINUS, self._character, self._current_line)
        elif self._is_token('\/'):
            token = Token(TokenType.DIVISION, self._character, self._current_line)
        elif self._is_token('\*'):
            token = Token(TokenType.MULTIPLICATION, self._character, self._current_line)
        elif self._is_token('\!'):
            if self.sefl_peek_character() == '=':
                token = self._make_two_character_token(TokenType.NOT_EQ)
            else:
                token = Token(TokenType.NEGATION, self._character, self._current_line)
        elif match(r'^$', self._character):
            token = Token(TokenType.EOF, self._character, self._current_line)
        elif self._is_token('\('):
            token = Token(TokenType.LPAREN, self._character, self._current_line)
        elif self._is_token('\)'):
            token = Token(TokenType.RPAREN, self._character, self._current_line)
        elif self._is_token('\{'):
            token = Token(TokenType.LBRACE, self._character, self._current_line)
        elif self._is_token('}'):
            token = Token(TokenType.RBRACE, self._character, self._current_line)
        elif self._is_token(','):
            token = Token(TokenType.COMMA, self._character, self._current_line)
        elif self._is_token(';'):
            token = Token(TokenType.SEMICOLON, self._character, self._current_line)
        elif self._is_token('<'):
            token = Token(TokenType.LT, self._character, self._current_line)
        elif self._is_token('>'):
            token = Token(TokenType.GT, self._character, self._current_line)
        elif self._is_letter(self._character):
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)
            #TODO ver si podemos volver al codigo donde no se hacia el return, 
            # se cambio por el problema el _read_caracter donde no pasaba la prueba 
            # test_function_declaration por no tener espacios en blanco entre la declaracion
            # del procedimiento y el ()
            return Token(token_type, literal, self._current_line)
        elif self._is_number_(self._character):
            literal = self._read_number()
            return Token(TokenType.INT, literal, self._current_line)
        elif match(r'^"$', self._character):
            literal = self._read_string()
            return Token(TokenType.STRING, literal, self._current_line)
        else:
            token = Token(TokenType.ILLEGAL, self._character, self._current_line)

        self._read_caracter()
        return token

    # Función que valida si el token enviado es igual al carácter actual. Esto se realiza con la función 
    # match por lo cual para poder evaluar los caracteres especiales que son parte de los utilizados para evaluar 
    # expresiones regulares se tendrá que utilizar el caracter de escape \
    def _is_token(self, token: str): # -> bool:
        return match(r'^' + token + '$', self._character)

    def _read_caracter(self):
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]
        
        if self._character == '\n':
            self._current_line +=1 

        self._position = self._read_position
        self._read_position += 1

    def _read_identifier(self) -> str:
        initial_position = self._position
        is_first_letter = True
        while self._is_letter(self._character) or \
                (not is_first_letter and self._is_number_(self._character)): 
            self._read_caracter()
            is_first_letter = False
        
        return self._source[initial_position:self._position]

    def _read_string(self) -> str:
        self._read_caracter()
        initial_position = self._position

        while self._character != '"' and self._read_position <= len(self._source):
            self._read_caracter()
        
        string = self._source[initial_position:self._position]
        self._read_caracter()
        return string
        
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
    def _skip_whitespace(self) -> None:
        while match(r'^\s$',self._character):
            self._read_caracter()

    def sefl_peek_character(self) -> str:
        if self._read_position >= len(self._source):
            return ''
        return self._source[self._read_position]
    
    def _make_two_character_token(self, token_type: TokenType) -> Token:
        prefix = self._character
        self._read_caracter()
        suffix = self._character

        return Token(token_type, f'{prefix}{suffix}', self._current_line)
