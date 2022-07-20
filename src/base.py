import os
from compiler.lexical import lexical_analysis
from compiler.sintax import SyntaxAnalyzer, SyntaxError

def compiler(filename):
    tokens = lexical_analysis(filename)
    tree = SyntaxAnalyzer(tokens).sintax_analysis()
    return tree

def print_list(lst, level=0):
    print('    ' * (level - 1) + '+---' * (level > 0) + str(lst))
    if hasattr(lst,'children'):
        for l in lst.children:
            if str(type(lst.children[0])) == "<class 'compiler.sintax.Tree'>":
                print_list(l, level + 1)
            else:
                print('    ' * level + '+---' + str(l))

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
        compiled_program = compiler(examples_path[1])
        # print(compiled_program)
        print_list(compiled_program)
    except SyntaxError as e:
        print(str(e))
    except Exception as e:
        raise e
