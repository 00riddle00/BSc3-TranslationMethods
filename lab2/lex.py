from sys import argv

from lexer.lexer import Lexer

file_to_lex = 'test.fx'
if len(argv) == 2:
    file_to_lex = argv[1]

with open(file_to_lex) as f:
    content = ''.join(f.readlines())

    try:
        lexer = Lexer(content)
        lexer.lex_all()

        lexer.print_tokens()
    except ValueError:
        pass
