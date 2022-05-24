from regular_expressions import RegexPatternMatching
import os

single_char_token_delimiters = ['+', '-', '*', '/', '<',  '>',  '=', ';', ',', '(', ')', '[',  ']', '{',  '}' ]
compound_token_delimiters = ['<=','>=', '==', '!=', '/*', '*/']
compound_first_char = ['<', '>', '=', '!', '/', '*']


def lexemize_file(filename):
    lexemes = []
    with open(filename) as f:
        line = f.readline()
        while line:
            curr_tkn = ""
            has_new_line = False
            for char in line:
                if char == " ":
                    if curr_tkn != "":
                        lexemes.append(curr_tkn)
                    curr_tkn = ""
                    continue
                elif char in compound_first_char:
                    if curr_tkn.isalpha() or curr_tkn.isnumeric():
                        lexemes.append(curr_tkn)
                        curr_tkn = char
                        continue
                    curr_tkn += char
                    continue
                elif curr_tkn in compound_token_delimiters:
                    lexemes.append(curr_tkn)
                    curr_tkn = char
                    continue
                elif  char in single_char_token_delimiters:
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
            if curr_tkn != "":
                lexemes.append(curr_tkn)
            if has_new_line:
                # lexemes.append('\n')
                has_new_line = False
            line = f.readline()
    return lexemes

if __name__ == '__main__':
    example_path = os.path.join(os.path.dirname(__file__), 'examples/sort.cminus')
    lexemes = lexemize_file(example_path)
    tokens = RegexPatternMatching().get_patterns_from_lexemes(lexemes)
    print(tokens)


# /*
#     Somebody once told me the world is gonna roll me
#     I ain't the sharpest tool in the shed
#     She was looking kind of dumb with her finger and her thumb
#     In the shape of an "L" on her forehead
# */