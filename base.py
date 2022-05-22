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
                # else:
                #     if '\n' in char:
                #         char = char.replace("\n", "")
                #         has_new_line = True
                #     curr_tkn += char
                #     continue
            # end of line processing
            if curr_tkn != "":
                lexemes.append(curr_tkn)
            if has_new_line:
                # lexemes.append('\n')
                has_new_line = False
            line = f.readline()
    print(lexemes)
    return lexemes


def tokenize_lexemes(lexemes):
    print('lexemes')


lexemize_file("example.txt")
