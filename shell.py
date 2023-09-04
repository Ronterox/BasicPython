import basic

while True:
    text = input('basic > ')
    result, error = basic.parse(text)

    print(error if error else result)