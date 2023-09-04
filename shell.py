import basic

quit_commands = ['quit()', 'exit()', 'q()', '.exit', '.quit']

while True:
    text = input('basic > ')
    if text in quit_commands:
        print('Exiting...')
        break
    result, error = basic.parse(text)

    print(error if error else result)
