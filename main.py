from string import ascii_letters
from enum import Enum


class Context(Enum):
    NONE = 0
    NEW_VAR = 1
    ASSIGN = 2
    USE_VAR = 3


DIGITS = '0123456789'
OPERATORS = '+-/*'
PARENTHESIS = '()'
LETTERS = ascii_letters
EQUAL = '='

linenum = 0

context: Context = Context.NONE

KEYWORDS = [
    "var"
]

# TODO: think about stack later
VARIABLES = {}

var = None


def def_variable(value):
    global var, context

    VARIABLES[var] = value
    context = Context.NONE
    var = None


def parse(line):
    global pos, char, linenum, context, var

    linenum += 1

    pos = -1
    char = None

    tokens = []
    errors = []

    # Slower but don't care
    add_token = lambda x: tokens.append(x)

    # Slower but don't care
    add_error = lambda x: errors.append(x)

    def advance():
        global pos, char

        pos = pos + 1
        char = line[pos] if pos < len(line) else None

    def add_num():
        num = ''
        dots = 0

        while char is not None and char in DIGITS + '.':
            if char == '.':
                if dots == 1: break
                dots += 1

            num += char
            advance()

        if context == Context.ASSIGN:
            def_variable(num)
        else:
            add_token(float(num) if dots == 1 else int(num))
        pass

    def add_operator():
        add_token(char)
        advance()
        pass

    def add_word():
        global context, var

        word = ''

        while char is not None and char in LETTERS:
            word += char
            advance()

        # TODO: Obviously switch this asap
        # TODO: Remove context from here, Add Tokens, Then Act line
        if context == Context.NONE:
            if word == 'var':
                context = Context.NEW_VAR
            elif word in VARIABLES.keys():
                context = Context.USE_VAR
                var = word
            else:
                # TODO: Add linenum automatically
                errors.append(f"Variable name {word} not found at line {linenum}")
        elif context == Context.NEW_VAR:
            if word not in VARIABLES.keys():
                var = word
            else:
                errors.append(f"Redefining variable of name {word}")
        elif context == Context.ASSIGN:
            def_variable(word)
        else:
            errors.append(f"Context not expected error at line {linenum}. Context: {context}")

    def add_equal():
        global context

        advance()

        if char is None:
            errors.append(f'Expected assignment at line {linenum}')
        elif char == EQUAL:
            pass
        else:
            context = Context.ASSIGN

    # Adding Tokens ------------------------------------------------------------------------

    advance()

    # Slower but don't care
    switch = {
        ' \t': advance,
        DIGITS: add_num,
        OPERATORS: add_operator,
        PARENTHESIS: add_operator,
        LETTERS: add_word,
        EQUAL: add_equal
    }.items()

    while char is not None:
        actionated = False

        for val, action in switch:
            if char is not None and char in val:
                actionated = True
                action()

        if not actionated:
            add_error(f"Illegal Char \'{char}\' at line {linenum} !")
            advance()

    # Results ------------------------------------------------------------------------
    if errors:
        for e in errors: print(e, end=' ')
        # TODO: Clean all variables
    elif context == Context.USE_VAR:
        print(f'{var} = {VARIABLES[var]}')
        # TODO: this a method
        context = Context.NONE
        var = None
    else:
        expr = ''
        for val in tokens: expr += str(val)

        print(expr, end=' ')

        for op in OPERATORS:
            if op in tokens:
                try:
                    print('=', eval(expr), end='')
                except SyntaxError:
                    print(f"Incorrect syntax at line {linenum}!", end='')
                break


pass

if __name__ == '__main__':
    line = ""
    while line.lower() != "exit":
        line = input(f"\n[{linenum + 1}] Basic > ")
        parse(line)
