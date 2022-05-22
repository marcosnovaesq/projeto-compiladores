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


def lexemize_file():
    tokens = []
    with open("example.txt") as f:
        line = f.readline()
        while line:
            curr_tkn = ""
            has_new_line = False
            for char in line:
                if char == " ":
                    if curr_tkn != "":
                        tokens.append(curr_tkn)
                    curr_tkn = ""
                    continue
                # add more token delimiter and maybe array token delimiter
                elif char == "[" or char == "]" or char == "{" or char == "}" or char == "=" or char == "+" or char == "-" or char == ">" or char == "<":
                    if curr_tkn != "":
                        tokens.append(curr_tkn)
                    tokens.append(char)
                    curr_tkn = ""
                    continue
                else:
                    if '\n' in char:
                        char = char.replace("\n", "")
                        has_new_line = True
                    curr_tkn += char
                    continue
            # end of line processing
            if curr_tkn != "":
                tokens.append(curr_tkn)
            if has_new_line:
                tokens.append('\n')
                has_new_line = False
            line = f.readline()
    print(tokens)
    return tokens

lexemize_file()
