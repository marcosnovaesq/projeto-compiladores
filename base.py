example_numerical_token_definition = {'token_type': 'NUMBER', 'numerical_value': 234, 'string_value': '234'}
example_literal_token_definition = {'token_type': 'LITERAL', 'string_value': 'joaozinho'}
# add more examples above

tokens = []

with open("example.txt") as f:
    line = f.readline()
    while line:
        splitted_line = line.split()
        for index in range(len(splitted_line)):
            curr_word = splitted_line[index]
            tokens.append(curr_word)
        line = f.readline()
print(tokens)
