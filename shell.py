import basic

quit_commands: list[str] = ['quit()', 'exit()', 'q()', '.exit', '.quit']

while True:
    text: str = input('basic > ')
    if text in quit_commands:
        print('Exiting...')
        break

    result, error = basic.evaluate('<stdout>', text)
    print(error if error else result)
