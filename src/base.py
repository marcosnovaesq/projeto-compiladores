from regular_expressions import RegexPatternMatching
import os

single_char_token_delimiters = ['+', '-', '*', '/', '<',  '>',  '=', ';', ',', '(', ')', '[',  ']', '{',  '}' ]
compound_token_delimiters = ['<=','>=', '==', '!=', '/*', '*/']
compound_first_char = ['<', '>', '=', '!', '/', '*']


def lexemize_file(filename):
    lexemes = []
    with open(filename) as f:
        line = f.readline()
        is_on_comment = False
        curr_tkn = ""
        while line:
            for char in line: #    {\n
                if is_on_comment:
                    curr_tkn += char
                    if '*/' in curr_tkn:
                        is_on_comment = False
                        lexemes.append(curr_tkn)
                        curr_tkn = ""
                    continue
                elif char == " ":
                    if curr_tkn != "":
                        lexemes.append(curr_tkn)
                    curr_tkn = ""
                    continue
                elif char in compound_first_char: #char eh < #curr_tkn = 9
                    if curr_tkn.isalpha() or curr_tkn.isnumeric(): # /* asdffaf *
                        lexemes.append(curr_tkn)
                        curr_tkn = char
                        continue
                    curr_tkn += char
                    if curr_tkn == '/*':
                        is_on_comment=True
                    continue
                elif curr_tkn in compound_token_delimiters:
                    lexemes.append(curr_tkn)
                    curr_tkn = char
                    continue
                elif char in single_char_token_delimiters:
                    if curr_tkn != "":
                        lexemes.append(curr_tkn)
                    lexemes.append(char)
                    curr_tkn = ""
                    continue
                elif char.isalpha(): 
                    curr_tkn += char
                    continue
                elif char.isnumeric():
                    curr_tkn += char
                    continue
            if curr_tkn != "" and not is_on_comment:
                lexemes.append(curr_tkn)
                curr_tkn = ""
            line = f.readline()
    return lexemes

if __name__ == '__main__':
    examples_path = {
        1: os.path.join(os.path.dirname(__file__), 'examples/sort.cminus'),
        2: os.path.join(os.path.dirname(__file__), 'examples/teste_comentario_simples.cminus'),
        3: os.path.join(os.path.dirname(__file__), 'examples/teste_comentario_varias_linhas.cminus'),
        4: os.path.join(os.path.dirname(__file__), 'examples/teste_comentario.cminus')
    }
    
    lexemes = lexemize_file(examples_path[1])
    tokens = RegexPatternMatching().get_patterns_from_lexemes(lexemes)
    print(tokens)
