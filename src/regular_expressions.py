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
        ('MISMATCH', r'.')  # ANOTHER CHARACTER
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
            token = self.get_pattern_rule_from_string(lex)
            if token != 'COMMENT':
                tokens_list.append((lex, self.get_pattern_rule_from_string(lex)))
        
        return tokens_list

    def search_for_mismatchs(self, lexemes: List[str]) -> List[str]:
        tokens = self.get_patterns_from_lexemes(lexemes)
        for index, token in enumerate(tokens):
            if token == 'MISMATCH':
                print(lexemes[index])
            