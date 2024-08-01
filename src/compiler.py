from lexer import Lexer
from parser import Parser

target = "dist/"

def compile(path: str, output: str):
    with open(path, "r") as f:
        code = f.read()

    # Tokenize
    lexer = Lexer()
    tokens = lexer.tokenize(code)
    tokens_list = list(tokens)
    # lexer.pprint(tokens_list)

    # Parse to AST
    parser = Parser()
    parser.parse(token for token in tokens_list)
    ast = parser.ast

    parser.pprint(ast)


if __name__ == "__main__":
    # compile("examples/variable.bl", target + "output.ml")
    # compile("examples/pointers.bl", target + "output.ml")
    # compile("examples/function.bl", target + "output.ml")
    compile("examples/match.bl", target + "output.ml")
