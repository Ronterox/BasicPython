DIGITS = '0123456789'
OPERATORS = '+-/*'
PARENTHESIS = '()'

linenum = 0


def parse(line):
    global pos, char, linenum

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

        add_token(float(num) if dots == 1 else int(num))
        pass

    def add_operator():
        add_token(char)
        advance()
        pass

    # Adding Tokens ------------------------------------------------------------------------

    advance()

    # Slower but don't care
    switch = {
        ' \t': advance,
        DIGITS: add_num,
        OPERATORS: add_operator,
        PARENTHESIS: add_operator
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
