from enum import Enum
from string import ascii_letters as LETTERS, digits as DIGITS, whitespace as WHITESPACE


class Type(Enum):
    INT = 'int'
    FLOAT = 'float'
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    LPAR = '('
    RPAR = ')'


TokenValue = str | float | int | None


class Error:
    def __init__(self, error: str, details: str) -> None:
        self.error: str = error
        self.details: str = details

    def __repr__(self) -> str:
        return f'{self.error}: {self.details}'


class IllegalCharError(Error):
    def __init__(self, details: str) -> None:
        super().__init__('Illegal Character', details)


class Token:
    def __init__(self, type_: Type, value: TokenValue = None) -> None:
        self.type: Type = type_
        self.value: TokenValue = type_.value if not value else value

    def __repr__(self) -> str:
        return f'{self.type.name}:{self.value}'


class Lexer:
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.pos: int = 0
        self.current_char: str | None = self.text[self.pos]

    def advance(self) -> None:
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def go_back(self) -> None:
        self.pos -= 1
        self.current_char = self.text[self.pos] if self.pos > -1 else None

    def make_tokens(self) -> tuple[list[Token], Error | None]:
        tokens: list[Token] = []

        while self.current_char != None:
            char: str = self.current_char
            match char:
                case char if char in WHITESPACE:
                    pass
                case char if char in DIGITS:
                    tokens.append(self.make_number())
                case Type.PLUS.value | Type.MINUS.value | Type.MUL.value | Type.DIV.value:
                    tokens.append(Token(Type(char)))
                case Type.LPAR.value | Type.RPAR.value:
                    tokens.append(Token(Type(char)))
                case _:
                    return [], IllegalCharError(char)
            self.advance()

        return tokens, None

    def make_number(self) -> Token:
        num: str = ""
        dots: int = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dots == 1:
                    break
                dots += 1
            num += self.current_char
            self.advance()
        
        if self.current_char != None:
            self.go_back()

        return Token(Type.FLOAT, float(num)) if dots == 1 else Token(Type.INT, int(num))


def parse(text: str) -> tuple[list[Token], Error | None]:
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error


if __name__ == "__main__":
    print(parse('1 + 2 * 3'))
