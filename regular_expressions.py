import re


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