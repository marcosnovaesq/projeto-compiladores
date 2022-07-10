from utils.logger import logger

class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__(f'Syntax error: {message}')

class Tree():
    def __init__(self, type, value='non-terminal', children = []):
        self.type = type
        self.children = children
        self.value = value

    def append_child(self, value): #value deve ser do tipo Tree
        self.children.append(value)

class SyntaxAnalyzer():
    def __init__(self, tokens):
        self.index = 0
        self.current_token = None
        self.tokens = tokens
        self.root = None

    def get_token(self):
        '''
        Controla o token corrente. Sempre que quisermos analisar um novo token, precisamos chamar essa função
        '''
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            raise SyntaxError('Out of bounds')

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.get_token()
        else:
            raise SyntaxError(f'[MATCH] Unexpected token {self.current_token}')

    def type_specifier(self):
        if self.current_token == 'int':
            return 'int'
        if self.current_token == 'void':
            return 'void'
        raise SyntaxError(f'[TYPE SPECIFIER] Expected a type identifier but got a {self.current_token}')

    def declaration(self):
        type_spec = self.type_specifier()
        self.match


        return None

    def declaration_list(self):
        self.root = Tree('declaration-list')
        self.get_token()
        d = self.declaration()
        while d is not None:
            self.root.append_child(d)
            d = self.declaration()
        
    def sintax_analysis(self):
        '''
        Temos uma lista de tuplas
        Cada tupla contem o token e o que representa o token no código

        Ideias: Adcionar um token de final de arquivo no final da lista de tokens na analise léxica.
        - Se não fechou um lexema e já lemos o final do arquivo -> deu ruim
        '''
        logger.info('Inicializando análise sintática')
        return self.declaration_list()



