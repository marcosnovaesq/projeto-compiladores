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
                # empty space 
                if char == " ":
                    if curr_tkn != "":
                        lexemes.append(curr_tkn)
                    curr_tkn = ""
                    continue
                elif char in compound_first_char and curr_tkn == "":
                    curr_tkn += char
                    continue
                elif char in compound_first_char and curr_tkn != "":
                    lexemes.append(curr_tkn + char)
                    curr_tkn = ""
                    continue
                elif (curr_tkn + char) in compound_token_delimiters:
                    curr_tkn += char
                    lexemes.append(curr_tkn)
                    curr_tkn = ""
                    continue
                elif (curr_tkn + char) not in compound_token_delimiters and char in single_char_token_delimiters:
                    if curr_tkn != "":
                        lexemes.append(curr_tkn)
                    lexemes.append(char)
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
