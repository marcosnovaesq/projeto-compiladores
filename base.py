
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
