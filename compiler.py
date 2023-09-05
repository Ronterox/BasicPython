import basic
from sys import argv

if len(argv) < 2:
    print("Usage: py compiler.py [file1] [file...n]")
    exit()

for filepath in argv[1:]:
    with open(filepath) as file:
        result, error = basic.parse(filepath, file.read())
        if error:
            print(error)
        else:
            print(result)
