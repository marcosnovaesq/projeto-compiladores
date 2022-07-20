import re
from typing import List


class RegexPatternMatching():
    rules = [
        ('COMMENT',r'\/\*(.|\n|\r|\n\r|\r\n)*\*\/'),
        ('ELSE', r'else'),  # else
        ('IF', r'if'),  # if
        ('INT', r'int'),  # int
        ('RETURN', r'return'),
        ('VOID', r'void'),
        ('WHILE', r'while'),  # while
        # ('OPEN_COMMENT',r'\/\*'),
        # ('CLOSE_COMMENT',r'\*\/'),
        ('PLUS', r'\+'),  # +
        ('MINUS', r'-'),  # -
        ('MULT', r'\*'),  # *
        ('DIV', r'\/'),  # /
        ('LT', r'<'),  # <
        ('LE', r'<='),  # <=
        ('GT', r'>'),  # >
        ('GE', r'>='),  # >=
        ('EQ', r'=='),  # ==
        ('NE', r'!='),  # !=
        ('ATTR', r'\='),  # =
        ('COMMA', r','),  # ,
        ('PCOMMA', r';'),  # ;
        ('LBRACKET', r'\('),  # (
        ('RBRACKET', r'\)'),  # )
        ('LSQRBRACKET', r'\['),  # [
        ('RSQRBRACKET', r'\]'),  # ]
        ('LBRACE', r'\{'),  # {
        ('RBRACE', r'\}'),  # }
        ('NUMBER', r'[0-9]+'),  # }
        ('ID', r'[a-zA-Z]+'),  # IDENTIFIERS
        # ('NEWLINE', r'\n'),  # NEW LINE
        # ('SKIP', r'[ \t]+'),  # SPACE and TABS
        ('MISMATCH', r'.+')  # ANOTHER CHARACTER
    ]

    def __init__(self):
        self.compiled_rules = self.compile_regex_rules()

    def compile_regex_rules(self):
        return {
            rule_name: re.compile(pattern) 
            for rule_name, pattern in self.rules
        }
    
    def get_pattern_rule_from_string(self, pattern_string: str) -> str or None:
        for rule, pattern in self.compiled_rules.items():
            if pattern.fullmatch(pattern_string):
                return rule
        
        return None

    def get_patterns_from_lexemes(self, lexemes: List[str]) -> List[str]:
        tokens_list = []
        for lex in lexemes:
            token = self.get_pattern_rule_from_string(lex[0])
            if token != 'COMMENT':
                tokens_list.append((lex[0], self.get_pattern_rule_from_string(lex[0]), lex[1]))
        
        return tokens_list

    def search_for_mismatchs(tokens):
        for token in tokens:
            if token[1] == 'MISMATCH':
                raise Exception("UNKNOWN VALUE {token} IN LINE {line}".format(token=token[0], line=token[2]))
            

def lexemize_file(filename):
    single_char_token_delimiters = ['+', '-', '*', '/', '<',  '>',  '=', ';', ',', '(', ')', '[',  ']', '{',  '}' ]
    compound_token_delimiters = ['<=','>=', '==', '!=', '/*', '*/']
    compound_first_char = ['<', '>', '=', '!', '/', '*']
    lexemes = []
    with open(filename) as f:
        line = f.readline()
        line_no = 1
        is_on_comment = False
        curr_tkn = ""
        while line:
            for char in line: #    {\n
                if is_on_comment:
                    curr_tkn += char
                    if '*/' in curr_tkn:
                        is_on_comment = False
                        lexemes.append((curr_tkn,line_no))
                        curr_tkn = ""
                    continue
                elif char == " ":
                    if curr_tkn != "":
                        lexemes.append((curr_tkn,line_no))
                    curr_tkn = ""
                    continue
                elif char in compound_first_char: #char eh < #curr_tkn = 9
                    if curr_tkn.isalpha() or curr_tkn.isnumeric(): # /* asdffaf *
                        lexemes.append((curr_tkn,line_no))
                        curr_tkn = char
                        continue
                    curr_tkn += char
                    if curr_tkn == '/*':
                        is_on_comment=True
                    continue
                elif curr_tkn in compound_token_delimiters:
                    lexemes.append((curr_tkn,line_no))
                    curr_tkn = char
                    continue
                elif char in single_char_token_delimiters:
                    if curr_tkn != "":
                        lexemes.append((curr_tkn,line_no))
                    lexemes.append((char,line_no))
                    curr_tkn = ""
                    continue
                elif char.isalpha(): 
                    curr_tkn += char
                    continue
                elif char.isnumeric():
                    curr_tkn += char
                    continue
            if curr_tkn != "" and not is_on_comment:
                lexemes.append((curr_tkn,line_no))
                curr_tkn = ""
            line = f.readline()
            line_no += 1
    return lexemes

def add_eof(tokens):
    last_line = tokens[-1][-1]
    tokens.append(
        ('EOF', 'EOF', last_line+1)
    )

def lexical_analysis(filename):
    lexemes = lexemize_file(filename)
    tokens = RegexPatternMatching().get_patterns_from_lexemes(lexemes)
    RegexPatternMatching.search_for_mismatchs(tokens)
    add_eof(tokens)
    return tokens