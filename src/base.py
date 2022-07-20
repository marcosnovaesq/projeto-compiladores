import os
from compiler.lexical import lexical_analysis
from compiler.sintax import SyntaxAnalyzer


def compiler(filename):
    tokens = lexical_analysis(filename)
    tree = SyntaxAnalyzer(tokens).sintax_analysis()
    return tree

if __name__ == '__main__':
    examples_path = {
        1: os.path.join(os.path.dirname(__file__), 'examples/sort.cminus'),
        2: os.path.join(os.path.dirname(__file__), 'examples/teste_comentario_simples.cminus'),
        3: os.path.join(os.path.dirname(__file__), 'examples/teste_comentario_varias_linhas.cminus'),
        4: os.path.join(os.path.dirname(__file__), 'examples/teste_comentario.cminus'),
        5: os.path.join(os.path.dirname(__file__), 'examples/analise_sintatica/declaracao.cminus'),
        6: os.path.join(os.path.dirname(__file__), 'examples/analise_sintatica/errado_declaracao.cminus')
    }
    
    try:
        compiled_program = compiler(examples_path[6])
        print(compiled_program)
    except Exception as e:
        print(str(e))
