import re

example_numerical_token_definition = {
    'token_type': 'NUMBER',
    'string_value': '234'
}
example_literal_token_definition = {
    'token_type': 'LITERAL',
    'string_value': 'joaozinho'
}
# add more examples above

tokens = []

rules = [
    ('MAIN', r'main'),  # main
    ('INT', r'int'),  # int
    ('FLOAT', r'float'),  # float
    ('IF', r'if'),  # if
    ('ELSE', r'else'),  # else
    ('WHILE', r'while'),  # while
    ('READ', r'read'),  # read
    ('PRINT', r'print'),  # print
    ('LBRACKET', r'\('),  # (
    ('RBRACKET', r'\)'),  # )
    ('LBRACE', r'\{'),  # {
    ('RBRACE', r'\}'),  # }
    ('COMMA', r','),  # ,
    ('PCOMMA', r';'),  # ;
    ('EQ', r'=='),  # ==
    ('NE', r'!='),  # !=
    ('LE', r'<='),  # <=
    ('GE', r'>='),  # >=
    ('OR', r'\|\|'),  # ||
    ('AND', r'&&'),  # &&
    ('ATTR', r'\='),  # =
    ('LT', r'<'),  # <
    ('GT', r'>'),  # >
    ('PLUS', r'\+'),  # +
    ('MINUS', r'-'),  # -
    ('MULT', r'\*'),  # *
    ('DIV', r'\/'),  # /
    ('ID', r'[a-zA-Z]\w*'),  # IDENTIFIERS
    ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),  # FLOAT
    ('INTEGER_CONST', r'\d(\d)*'),  # INT
    ('NEWLINE', r'\n'),  # NEW LINE
    ('SKIP', r'[ \t]+'),  # SPACE and TABS
    ('MISMATCH', r'.'),  # ANOTHER CHARACTER
]

with open("example.txt") as f:
    line = f.readline()
    while line:
        curr_tkn = ""
        for char in line:
            # tkn_delimiters
            if char == " ":
                # process token and continue
                if curr_tkn != "":
                    tokens.append(curr_tkn)
                continue
            elif char == "[" or char == "]" or char == "{" or char == "}" or char == "=" or char == "+" or char == "-":
                if curr_tkn != "":
                    tokens.append(curr_tkn)
                tokens.append(char)
                curr_tkn = ""
                # process old token and add this token
                continue
            else:
                curr_tkn += char
                continue
        tokens.append(curr_tkn)
        # splitted_line = line.replace(" ", "")
        # tokens.append(splitted_line)
        line = f.readline()
print(tokens)
