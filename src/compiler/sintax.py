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
        if self.current_token[1] == expected_token:
            current_token_value = self.current_token[0]
            self.get_token()
            return current_token_value
        else:
            raise SyntaxError(f'[MATCH] Unexpected token {self.current_token}')

    def type_specifier(self):
        if self.current_token[1] == 'INT' | self.current_token[1] == 'VOID' :
            token = self.current_token
            self.get_token()
            return token

        raise SyntaxError(f'[TYPE SPECIFIER] Expected a type identifier but got a {self.current_token}')

    def param(self):
        type_spec = self.type_specifier()
        id_value = self.match('ID')
        t = Tree('param')

        if self.current_token[1] == 'LSQRBRACKET':
            self.match('LSQRBRACKET')
            self.match('RSQRBRACKET')
            t.append()
            return Tree('param', children=[
                Tree('type-specifier', children=[Tree(type_spec[1], value=type_spec[0])]),
                Tree('ID', value=id_value),
                Tree('param-linha', children=[
                    Tree('LSQRBRACKET', '['),
                    Tree('RSQRBRACKET', ']'),
                ])
            ])
        else:
            return Tree('param', children=[
                Tree('type-specifier', children=[Tree(type_spec[1], value=type_spec[0])]),
                Tree('ID', value=id_value),
            ])

    def param_list(self):
        param_list_node = Tree('param-list')
        
        node = self.param()

        while node is not None and self.current_token[1] == 'COMMA':
            param_list_node.append_child(node)
            self.match('COMMA')
            node = self.param()

        return param_list_node
            
    def params(self):
        t = Tree('params')
        if self.current_token[1] == 'VOID':
            void = self.match('VOID')
            t.append_child(Tree('VOID', void))
            return t
        
        t.append(self.param_list())
        return t

    def compound_stmt(self):

        pass

    def declaration(self):
        '''
        A declaração de uma função ou variavel
        Primeiro precisa ser int ou void
        depois tem que ser um ID
        se der match no tipo e no ID, logo em sequência deve vir:
            ou ponto-e-vírgula PCOMMA
            ou abertura de colchetes LSQRBRACKET
            ou abertura de parenteses LBRACKET
        
        TODO: passar esses tokens pra um ENUM. Ta muito propenso a erro dessa forma
        '''
        type_spec = self.type_specifier()
        id_value = self.match('ID')
        t = Tree('declaration')

        if self.current_token[1] == 'PCOMMA':
            new_t = Tree('var-declaration', children=[
                Tree('type-specifier', children=[Tree(type_spec[1], value=type_spec[0])]),
                Tree('ID', value=id_value),
                Tree('PCOMMA', ';')
            ])
            t.append_child(new_t)
            self.match('PCOMMA')
            return t

        if self.current_token[1] == 'LSQRBRACKET':
            self.match('LSQRBRACKET')
            number = self.match('NUMBER')
            self.match('RSQRBRACKET')
            self.match('PCOMMA')

            t.append_child(
                Tree('var-declaration', children=[
                    Tree('type-specifier', children=[Tree(type_spec[1], value=type_spec[0])]),
                    Tree('ID', value=id_value),
                    Tree('var-declaration-linha', children=[
                        Tree('LSQRBRACKET','['),
                        Tree('NUMBER',number),
                        Tree('RSQRBRACKET',']'),
                        Tree('PCOMMA',';')
                    ]),
                ])
            )

            return t

        if self.current_token[1] == 'LBRACKET':
            self.match('LBRACKET')
            new_t = Tree('fun-declaration', children=[
                Tree('type-specifier', children=[Tree(type_spec[1], value=type_spec[0])]),
                Tree('ID', value=id_value),
                Tree('LBRACKET', '('),
                self.params(),
                Tree('RBRACKET', ')'),
                self.compound_stmt()
            ])
            return new_t

        if self.current_token is not None:
            raise SyntaxError(f'unexpected token {self.current_token}')

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



