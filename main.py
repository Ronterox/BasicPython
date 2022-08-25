from string import ascii_letters

# TODO: have aliases alias instead of #Define

DIGITS = '0123456789'
OPERATORS = '+-/*'
PARENTHESIS = '()'
LETTERS = ascii_letters
EQUAL = '='

linenum = 0

KEYWORDS = [
    'exit',
    'var'
]

parenthesis = -1

VARIABLES = {}
FUNCTIONS = {}


def parse(line):
    global pos, char, linenum, parenthesis

    linenum += 1

    pos = -1
    char = None

    tokens = []
    errors = []

    # Slower but don't care
    add_token = lambda t: tokens.append(t)

    # Slower but don't care
    add_error = lambda e: errors.append(f'Error at line {linenum}: {e}')

    def advance():
        global pos, char

        pos = pos + 1
        char = line[pos] if pos < len(line) else None

    def add_num():
        num = ''
        dots = 0

        while char is not None and char in DIGITS + '.':
            if char == '.':
                if dots == 1:
                    add_error("Extra dot found!")
                    break
                dots += 1

            num += char
            advance()

        add_token(float(num) if dots == 1 else int(num))

    def add_operator():
        add_token(char)
        advance()

        if char is None:
            errors.append(f"Expected assignment!")

    def add_parenthesis():
        global parenthesis

        parenthesis += 1 if char == '(' else -1

        add_token(char)
        advance()

    def add_word():
        word = ''

        while char is not None and char in LETTERS:
            word += char
            advance()

        add_token(word)

    # Adding Tokens ------------------------------------------------------------------------

    advance()

    # Slower but don't care
    switch = {
        ' \t': advance,
        DIGITS: add_num,
        OPERATORS: add_operator,
        PARENTHESIS: add_parenthesis,
        LETTERS: add_word,
        EQUAL: add_operator
    }.items()

    while char is not None:
        actionated = False

        for tok, action in switch:
            if char is not None and char in tok:
                actionated = True
                action()

        if not actionated:
            add_error(f"Illegal Char '{char}'!")
            advance()

    if parenthesis != -1:
        parenthesis = -1
        add_error("Incorrect Parenthesis!")

    # Results ------------------------------------------------------------------------
    expr = ''
    for tok in tokens: expr += str(tok)

    result = None

    if errors:
        for e in errors: print(e, end=' ')
        errors.clear()
    else:
        split = expr.strip().split('=')

        size = len(split)

        if size > 2:  # Error
            add_error("Incorrect expression!")

        elif size > 1:  # Assignment
            left, right = split

            def assign():
                try:
                    return exec(left + '=' + str(eval(right, VARIABLES)), VARIABLES)
                except SyntaxError:
                    add_error("Syntax error!")
                    return None

            # TODO: print assign statements better
            if left.startswith(KEYWORDS[1]):
                left = left[len(KEYWORDS[1]):]
                if left in VARIABLES:
                    add_error(f"Redefining variable {left}!")
                else:
                    result = assign()
            elif left in VARIABLES:
                result = assign()
            else:
                add_error(f"Variables {left} is not defined!")

        else:  # Execution
            try:
                if split[0] in VARIABLES:
                    result = exec(split[0], FUNCTIONS) if split[0] in FUNCTIONS else VARIABLES[split[0]]
                else:
                    for op in OPERATORS:
                        if op in split[0]:
                            result = eval(split[0], VARIABLES)
            except SyntaxError:
                add_error("Syntax error!")

        if errors:
            for e in errors: print(e, end=' ')

    print(expr + f' = {str(result)}' if result else expr)


if __name__ == '__main__':
    line = ''
    while line.lower() != KEYWORDS[0]:
        line = input(f"\n[{linenum + 1}] Basic > ")
        parse(line)
