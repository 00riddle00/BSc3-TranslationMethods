from pprint import pprint

KEYWORDS = {
    'fx': 'KW_FN',
    'if': 'KW_IF',
    'elif': 'KW_ELIF',
    'else': 'KW_ELSE',
    'for': 'KW_FOR',
    'while': 'KW_WHILE',
    'break': 'KW_BREAK',
    'continue': 'KW_CONTINUE',
    'return': 'KW_RETURN',
    'int': 'KW_INT',
    'float': 'KW_FLOAT',
    'bool': 'KW_BOOL',
    'char': 'KW_CHAR',
    'string': 'KW_STRING',
    'struct': 'KW_STRUCT',
}


class Input:

    name: str
    text: str
    offset: int
    curr_ln: int
    first_ln: int
    size: int

    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.size = len(text)
        self.offset = 0
        self.curr_ln = 1
        self.first_ln = 1

    def read_char(self):
        char = self.text[self.offset]
        self.offset += 1
        return char

    def reverse_read(self, delta=1):
        self.offset -= delta

    def is_input_read(self):
        return self.offset >= self.size


class Token:

    type_: str
    value: str
    line_no: int

    def __init__(self, type_, value, line_no):
        self.type = type_
        self.value = value
        self.line_no = line_no


class Lexer:
    inputs: list
    curr_input: Input
    buffer: str
    state: str
    tokens: list
    running: bool
    curr_char: str

    def __init__(self, inputs) -> None:
        if type(inputs) == list:
            self.inputs = [inputs]
        elif type(inputs) == Input:
            self.inputs = [inputs]
        else:
            self.lexer_error('Wrong input passed to lexer constructor.')

        self.buffer = ''
        self.line_no = 1
        self.offset = 0
        self.state = 'START'
        self.tokens = []
        self.token_start = 0
        self.token_start_ln = 1
        self.running = True
        self.curr_char = ''

    def add(self):
        self.buffer += self.curr_char

    def begin_token(self, new_state):
        self.token_start_ln = self.line_no
        self.state = new_state

    def complete_ident(self):
        self.curr_input.reverse_read()

        if self.buffer in KEYWORDS:
            kw_type = KEYWORDS[self.buffer]
            self.buffer = ''
            self.complete_token(kw_type)
        else:
            self.complete_token('IDENT')

    def complete_token(self, token_type, reverse=False, delta=0):
        self.tokens.append(
            Token(token_type, self.buffer, self.curr_input.first_ln))
        self.buffer = ''
        self.state = 'START'
        if reverse:
            self.curr_input.reverse_read(delta)

    def dump_tokens(self):
        print(f'{"ID":>3}| {"LN":>3}| {"TYPE":<14} | {"VALUE":<14}')
        for index, token in enumerate(self.tokens):
            print(f'{index:>3}|'
                  f' {token.line_no:>3}|'
                  f' {token.type:<14} |'
                  f' {token.value:<14}')

    def lex_all(self):

        for _input in self.inputs:
            self.curr_input = _input

            # uncomment for debugging
            print(81*'#')
            pprint(self.curr_input.text)
            print(81*'#')

            while self.running and not self.curr_input.is_input_read():
                self.curr_char = self.curr_input.read_char()
                self.lex_char()

            self.curr_char = 'EOF'

            if self.state == 'START':
                self.complete_token('EOF')
            else:
                self.lex_char()

            if self.state == 'LIT_STR':
                self.lexer_error('unterminated string')

            # if self.running:
            #     self.curr_char = '\n'
            #     self.lex_char()
            # if self.state != 'START'
            #     self.lexer_error(f'unterminated something {self.state}', None)

            # else:
            #     self.lexer_error(f'unterminated token: {self.state}')

            # if self.state == 'START':
            #     self.complete_token('EOF')
            # elif self.state == 'LIT_STR':
            #     self.lexer_error('unterminated string')
            # else:
            #     self.lexer_error(f'unterminated token: {self.state}')

    def lex_char(self):
        if self.state == 'COMMENT_SL':
            self.lex_comment_sl()
        elif self.state == 'IDENT':
            self.lex_ident()
        elif self.state == 'LIT_INT':
            self.lex_lit_int()
        elif self.state == 'LIT_STR':
            self.lex_lit_str()
        elif self.state == 'LIT_STR_ESCAPE':
            self.lex_lit_str_escape()
        elif self.state == 'OP_L':
            self.lex_op_l()
        elif self.state == 'START':
            self.lex_start()
        else:
            raise Exception(f'invalid state {self.state}')

    def lex_comment_sl(self):
        if self.curr_char == '\n':
            self.line_no += 1
            self.state = 'START'
        else:
            pass  # ignore

    def lex_ident(self):
        if self.is_letter():
            self.add()
        elif self.is_digit():
            self.add()
        elif self.curr_char == '_':
            self.add()
        else:
            self.complete_ident()

    def lex_lit_int(self):
        if self.is_digit():
            self.add()
        else:
            self.curr_input.reverse_read()
            self.complete_token('LIT_INT')

    def lex_lit_str(self):
        if self.curr_char == '"':
            self.complete_token('LIT_STR')
        elif self.curr_char == '\\':
            self.state = 'LIT_STR_ESCAPE'
        elif self.curr_char == '\n':
            self.add()
            self.line_no += 1
        else:
            self.add()

    def lex_lit_str_escape(self):
        if self.curr_char == '"':
            self.buffer += '"'
        elif self.curr_char == 't':
            self.buffer += "\t"
        elif self.curr_char == 'n':
            self.buffer += "\n"
        elif self.curr_char == "\\":
            self.buffer += "\\"
        else:
            self.lexer_error('invalid_escape symbol', self.curr_char)
        self.state = 'LIT_STR'

    def lex_op_l(self):
        if self.curr_char == '=':
            self.complete_token('OP_LE')
        else:
            self.curr_input.reverse_read()
            self.complete_token('OP_L')

    def lex_start(self):
        if self.is_letter():
            self.add()
            self.begin_token('IDENT')
        elif self.curr_char == '_':
            self.add()
            self.begin_token('IDENT')
        elif self.is_digit():
            self.add()
            self.begin_token('LIT_INT')  # FIX
        elif self.curr_char == '"':
            self.begin_token('LIT_STR')
        elif self.curr_char == '#':
            self.state = 'COMMENT_SL'
        elif self.curr_char == ' ':
            pass  # ignore
        elif self.curr_char == '\n':
            self.line_no += 1
        elif self.curr_char == '\t':
            pass  # ignore
        elif self.curr_char == '+':
            self.begin_token('START')
            self.complete_token('OP_PLUS')
        elif self.curr_char == '<':
            self.begin_token('OP_L')  # delta = -1
        elif self.curr_char == '<':
            self.begin_token('OP_G')  # delta = -1
        elif self.curr_char == '=':
            self.begin_token('START')
            self.complete_token('OP_E')
        elif self.curr_char == '-':
            self.begin_token('START')
            self.complete_token('OP_SUB')
        elif self.curr_char == '*':
            self.begin_token('START')
            self.complete_token('OP_MUL')
        elif self.curr_char == '/':
            self.begin_token('START')
            self.complete_token('OP_DIV')
        elif self.curr_char == '(':
            self.begin_token('START')
            self.complete_token('OP_PAREN_O')
        elif self.curr_char == ')':
            self.begin_token('START')
            self.complete_token('OP_PAREN_C')
        elif self.curr_char == '{':
            self.begin_token('START')
            self.complete_token('OP_BRACE_O')
        elif self.curr_char == '}':
            self.begin_token('START')
            self.complete_token('OP_BRACE_C')
        elif self.curr_char == ';':
            self.begin_token('START')
            self.complete_token('OP_SEMICOLON')
        elif self.curr_char == ',':
            self.begin_token('START')
            self.complete_token('OP_COMMA')
        else:
            self.lexer_error(item=self.curr_char)

    def is_letter(self):
        c = self.curr_char
        return len(c) == 1 and (ord(c) in range(ord('A'), ord('Z')+1) or ord(c) in range(ord('a'), ord('z')+1))

    def is_digit(self):
        return len(self.curr_char) == 1 and ord(self.curr_char) in range(ord('0'), ord('9')+1)

    def lexer_error(self, msg=None, item=None):
        top_right_delim = 33 * '!'
        top_left_delim = 33 * '!'
        v_delim = 5 * '!'
        bottom_delim = 81 * '!'

        print(f'{top_left_delim} [Lexer error] {top_right_delim}')
        print(f'{v_delim} [@] [inputName: {self.curr_input.name} '
              f'line: {self.curr_input.curr_ln} '
              f'position: {self.curr_input.offset}]')
        if not msg:
            msg = 'Something went wrong'
        print(f'{v_delim} [Error message]: {msg}'),
        if item:
            print(f'{v_delim} [Item being lexed]:\n')
            pprint(item)
        print(bottom_delim)

