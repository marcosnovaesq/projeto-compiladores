from re import S
from utils.logger import logger

class SyntaxError(Exception):
    def __init__(self, message, token):
        formatted_token_string = f'\nToken value: {token[0]}\nToken name: {token[1]}\nLine: {token[2]}'
        super().__init__(f'[Syntax Error] {message} {formatted_token_string}')

class Tree():
    def __init__(self, type, value='non-terminal', children = []):
        self.type = type
        self.children = children
        self.value = value

    def append_child(self, child): #value deve ser do tipo Tree
        self.children = [*self.children, child]

    def __str__(self):
        return f"{self.type} {self.value}"

class SyntaxAnalyzer():
    def __init__(self, tokens):
        self.index = 0
        self.current_token = None
        self.tokens = tokens

    def get_token(self):
        '''
        Controla o token corrente. Sempre que quisermos analisar um novo token, precisamos chamar essa função
        '''
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            raise SyntaxError('Out of bounds', self.current_token)

    def match(self, expected_token):
        if self.current_token[1] == expected_token:
            current_token_value = self.current_token[0]
            self.get_token()
            return current_token_value
        else:
            raise SyntaxError(f'[MATCH] Unexpected token. Token Expected {expected_token}', self.current_token)

    def type_specifier(self):
        if self.current_token[1] == 'INT' or self.current_token[1] == 'VOID' :
            token = self.current_token
            self.get_token()
            return token

        raise SyntaxError(f'[TYPE SPECIFIER] Expected a type identifier but got a {self.current_token[1]}', self.current_token)

    def param(self):
        type_spec = self.type_specifier()
        id_value = self.match('ID')
        t = Tree('param')

        if self.current_token[1] == 'LSQRBRACKET':
            self.match('LSQRBRACKET')
            self.match('RSQRBRACKET')
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
        param_list_node.append_child(node)

        while node is not None and self.current_token[1] == 'COMMA':
            self.match('COMMA')
            node = self.param()
            param_list_node.append_child(node)

        return param_list_node
            
    def params(self):
        t = Tree('params')
        if self.current_token[1] == 'VOID':
            void = self.match('VOID')
            t.append_child(Tree('VOID', void))
            return t
        
        t.append_child(self.param_list())
        return t

    def is_a_type(self, token_type):
        if token_type == 'INT' or token_type == 'VOID':
            return True
        return False

    def var_declaration(self):
        # TODO colocar essa função dentro do declaration
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

        raise SyntaxError(f'Unexpected token', self.current_token)

    def local_declarations(self):
        t = Tree('local-declarations')
        if self.is_a_type(self.current_token[1]):
            new_node = self.var_declaration()

        if new_node is not None:
            t.append_child(new_node)
            while self.is_a_type(self.current_token[1]):
                new_node = self.var_declaration()
                t.append_child(new_node)

        return t

    def arg_list(self):
        t = Tree('arg-list')

        node = self.expression()
        t.append_child(node)
        while self.current_token[1] == 'COMMA':
            self.match('COMMA')
            node = self.expression()
            t.append_child(node)
        
        return t

    def args(self):
        t = Tree('args')
        if self.current_token[1] != 'RBRACKET':
            t.append_child(
                self.arg_list()
            )
        return t

    def ident_statement(self):
        #TODO: Montar a arvore como na BNF
        id = self.match('ID')
        #term...

        t = Tree('term')
        id_node = Tree('ID', id)
        t.append_child(id_node)
        if self.current_token[1] == 'LBRACKET':
            self.match('LBRACKET')
            arguments = self.args()
            self.match('RBRACKET')

            t.append_child(Tree('LBRACKET', '('))
            t.append_child(arguments)
            t.append_child(Tree('RBRACKET', ')'))
            return t
        elif self.current_token[1] == 'LSQRBRACKET':
            self.match('LSQRBRACKET')
            expr = self.expression()
            self.match('RSQRBRACKET')

            t.append_child(Tree('LSQRBRACKET', '['))
            t.append_child(expr)
            t.append_child(Tree('RSQRBRACKET', ']'))
            return t

        return id_node

    def factor(self, left_value):
        t = Tree('factor')
        if left_value is not None:
            return left_value
        
        if self.current_token[1] == 'ID':
            node = self.ident_statement() #TOKEN var ou call
        elif self.current_token[1] == 'LBRACKET':
            self.match('LBRACKET')
            node = self.expression()
            self.match('RBRACKET')
        elif self.current_token[1] == 'NUMBER':
            node = Tree('NUMBER', value=int(self.current_token[0]))
            self.match('NUMBER')
        else:
            raise SyntaxError('[factor] unexpected token', self.current_token)

        t.append_child(node)

        return t

    def term(self, left_value):
        t = Tree('term')

        node = self.factor(left_value)
        if node is not None:
            t.append_child(node)

        while self.current_token[1] == 'MULT' or self.current_token[1] == 'DIV':
            self.match(self.current_token[1])
            node = self.factor(None)
            if node is not None:
                t.append_child(node)

        return t

    def additive_expression(self, left_value):
        t = Tree('additive-expression')

        node = self.term(left_value)
        if node is not None:
            t.append_child(node)

        while self.current_token[1] == 'PLUS' or self.current_token[1] == 'MINUS':
            self.match(self.current_token[1])
            node = self.term(None)
            if node is not None:
                t.append_child(node)
        
        return t

    def simple_expression(self, left_value):
        t = Tree('simple-expression')
        left_expression = self.additive_expression(left_value)

        if self.current_token[1] in ('LT', 'LE', 'GT', 'GE', 'EQ', 'NE'):
            operator = self.match(self.current_token[1])
            right_expression = self.additive_expression(None)
            t.append_child(left_expression)
            t.append_child(right_expression)
            t.type = operator
        else:
            t.append_child(left_expression)

        return t

    def expression(self):
        t = Tree('expression')
        got_l_value = False
        left_value = None
        if self.current_token[1] == 'ID':
            left_value = self.ident_statement()
            got_l_value = True
        
        if got_l_value and self.current_token[1] == 'ATTR':
            if left_value is not None:
                self.match('ATTR')
                right_value = self.expression()
                t.append_child(left_value)
                t.append_child(right_value)
            else:
                raise SyntaxError('Tentativa de atribuição inválida sem valor esquerdo', self.current_token)
        else:
            t.append_child(
                self.simple_expression(left_value)
            )

        return t
        
    def selection_statement(self):
        #TODO adcionar os não terminais em uma arvore e montar o selection-stmt
        logger.info('Entrou no selection statement')
        t = Tree('selection-stmt')

        self.match('IF')
        self.match('LBRACKET')
        expr = self.expression()
        self.match('RBRACKET')

        t.append_child(Tree('IF', 'if'))
        t.append_child(Tree('LBRACKET', '('))
        t.append_child(expr)
        t.append_child(Tree('RBRACKET', ')'))
        t.append_child(self.statement())

        if self.current_token[1] == 'ELSE':
            self.match('ELSE')
            t.append_child(self.statement())
        
        return t

    def iteration_statement(self):
        self.match('WHILE')
        self.match('LBRACKET')
        expression = self.expression()
        self.match('RBRACKET')
        statement = self.statement()

        return Tree('iteration-statement', children=[
            Tree('WHILE', 'while'),
            Tree('LBRACKET', '('),
            expression,
            Tree('RBRACKET', ')'),
            statement
        ])

    def return_statement(self):
        t = Tree('return-stmt')
        self.match('RETURN')
        t.append_child(Tree('RETURN', 'return'))


        if self.current_token[1] != 'PCOMMA':
            expression = self.expression()

        if expression is not None:
            t.append_child(expression)

        self.match('PCOMMA')
        t.append_child(Tree('PCOMMA', ';'))

        return t

    def expression_statement(self):
        t = Tree('expression-stmt')
        if self.current_token[1] == 'PCOMMA':
            self.match('PCOMMA')
            t.append_child(Tree('PCOMMA', ';'))
        elif self.current_token[1] != 'RBRACE':
            t.append_child(self.expression())
            self.match('PCOMMA')
            t.append_child(Tree('PCOMMA', ';'))
        
        return t


    def statement(self):
        t = Tree('statement')

        if self.current_token[1] == 'IF':
            t.append_child(
                self.selection_statement()
            ) 
        elif self.current_token[1] == 'WHILE':
            t.append_child(
                self.iteration_statement()
            ) 
        elif self.current_token[1] == 'RETURN':
            t.append_child(
                self.return_statement()
            )
        elif self.current_token[1] == 'LBRACE':
            t.append_child(
                self.compound_stmt()
            )
        elif self.current_token[1] in ('ID', 'PCOMMA', 'LBRACKET', 'NUMBER'):
            t.append_child(
                self.expression_statement()
            )
        else:
            raise SyntaxError(f'unexpected token', self.current_token)
            
        return t

    def statement_list(self):
        t = Tree('statement-list')
        if self.current_token[1] != 'RBRACE':
            node = self.statement()
            t.append_child(node)
            while self.current_token[1] != 'RBRACE':
                node = self.statement()
                t.append_child(node)

        return t

    def compound_stmt(self):
        t = Tree('compound-stmt', children=[
            Tree('LBRACE', '{')
        ])
        self.match('LBRACE')

        if self.current_token[1] != 'RBRACE':
            if self.is_a_type(self.current_token[1]):
                t.append_child(
                    self.local_declarations()
                )
            if self.current_token[1] != 'RBRACE':
                t.append_child(
                    self.statement_list()
                )

        self.match('RBRACE')
        t.append_child(Tree('RBRACE', '}'))
        return Tree

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
                
            ])
            self.match('RBRACKET')
            new_t.append_child(Tree('RBRACKET', ')'))
            new_t.append_child(self.compound_stmt())                
            return new_t

        if self.current_token is not None:
            raise SyntaxError(f'unexpected token', self.current_token)

        return t

    def declaration_list(self):
        root = Tree('declaration-list')

        self.get_token()
        d = self.declaration()
        root.append_child(d)
        while self.current_token[0] != 'EOF':
            root.append_child(self.declaration())
        
        return root
        
    def sintax_analysis(self):
        '''
        Temos uma lista de tuplas
        Cada tupla contem o token e o que representa o token no código

        Ideias: Adcionar um token de final de arquivo no final da lista de tokens na analise léxica.
        - Se não fechou um lexema e já lemos o final do arquivo -> deu ruim
        '''
        logger.info('Inicializando análise sintática')
        t = self.declaration_list()

        if self.current_token[0] != 'EOF':
            raise SyntaxError("EOF expected", self.current_token)

        return t
