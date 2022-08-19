DIGITS = '0123456789'
OPERATORS = '+-/*'

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

    advance()

    # Slower but don't care
    switch = {
        ' \t': advance,
        DIGITS: add_num,
        OPERATORS: add_operator
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

    print_list = errors if errors else tokens
    for token in print_list: print(token)
    pass


if __name__ == '__main__':
    line = ""
    while line.lower() != "exit":
        line = input("Basic > ")
        parse(line)
