from enum import Enum
from string import ascii_letters as LETTERS, digits as DIGITS, whitespace as WHITESPACE
from dataclasses import dataclass


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


class Token:
    def __init__(self, type_: Type, value: TokenValue = None) -> None:
        self.type: Type = type_
        self.value: TokenValue = type_.value if not value else value

    def __repr__(self) -> str:
        return f'{self.type.name}:{self.value}'


class Position:
    def __init__(self) -> None:
        self.line: int = 0
        self.col: int = 0
        self.idx: int = 0

    def advance(self, char: str | None) -> None:
        self.idx += 1
        self.col += 1
        if char == '\n':
            self.line += 1
            self.col = 0


@dataclass
class Details:
    info: str
    pos: Position
    filename: str


class Error:
    def __init__(self, error: str, details: Details) -> None:
        self.error: str = error
        self.details: Details = details

    def __repr__(self) -> str:
        return f'{self.error} on file {self.details.filename} at line {self.details.pos.line}, col {self.details.pos.col}: {self.details.info}'


class IllegalCharError(Error):
    def __init__(self, details: Details) -> None:
        super().__init__('Illegal Character', details)


class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.text: str = text
        self.pos: Position = Position()
        self.current_char: str | None = self.text[self.pos.col]
        self.filename: str = filename

    def advance(self) -> None:
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

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
                    pass
                case _:
                    return [], IllegalCharError(Details(f"'{char}'", self.pos, self.filename))

            if char not in DIGITS:  # Slower but cleaner
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

        return Token(Type.FLOAT, float(num)) if dots == 1 else Token(Type.INT, int(num))


def parse(filename: str, text: str) -> tuple[list[Token], Error | None]:
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()

    return tokens, error


if __name__ == "__main__":
    print(parse(__file__, '1 + 2 * 3'))
