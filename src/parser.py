import re
from typing import NoReturn

import sly

import lexer


class Parser(sly.Parser):
    tokens = lexer.Lexer.tokens

    def __init__(self):
        self.ast = []

    # Base
    @_("statements")
    def body(self, p):
        self.ast = p.statements

    @_("statement")
    def statements(self, p):
        return [p.statement]
    
    @_("statements statement")
    def statements(self, p):
        p.statements.append(p.statement)
        return p.statements
    
    @_("LPAR expr RPAR")
    def expr(self, p):
        return p.expr
    
    # Comments
    # @_("LINE_COMMENT")
    # def statement(self, p):
    #     return "LineComment", {"value": p.LINE_COMMENT}

    # @_("MULTILINE_COMMENT")
    # def statement(self, p):
    #     return "MultiLineComment", {"value": p.MULTILINE_COMMENT}
    
    # Variables
    @_("ID ID EQ expr SEMICOLON")
    def statement(self, p):
        return "Assign", {
            "type": p.ID0,
            "name": p.ID1,
            "value": p.expr
        }
    
    # Functions definition
    @_("ID ID LPAR def_params RPAR LBRA statements RBRA")
    def statement(self, p):
        return "Function", {
            "type": p.ID0,
            "name": p.ID1,
            "generic_types": [],
            "def_params": p.def_params,
            "body": p.statements
        }
    
    @_("ID ID LPAR def_params RPAR LBRA RBRA")
    def statement(self, p):
        return "Function", {
            "type": p.ID0,
            "name": p.ID1,
            "generic_types": [],
            "def_params": p.def_params,
            "body": []
        }
    
    # Functions definition with scopes
    @_("ID ID LT generic_types GT LPAR def_params RPAR LBRA statements RBRA")
    def statement(self, p):
        return "Function", {
            "type": p.ID0,
            "name": p.ID1,
            "generic_types": p.generic_types,
            "def_params": p.def_params,
            "body": p.statements
        }

    @_("ID ID LT generic_types GT LPAR def_params RPAR LBRA RBRA")
    def statement(self, p):
        return "Function", {
            "type": p.ID0,
            "name": p.ID1,
            "generic_types": p.generic_types,
            "def_params": p.def_params,
            "body": []
        }
    
    @_("ID")
    def generic_type(self, p):
        return {"type": p.ID}

    @_("generic_types COMMA ID")
    def generic_types(self, p):
        p.generic_types.append({"type": p.ID})
        return p.generic_types

    @_("generic_type")
    def generic_types(self, p):
        return [p.generic_type]

    # Return statement
    @_("RETURN expr SEMICOLON")
    def statement(self, p):
        return "Return", {"value": p.expr}

    # Function params
    @_("ID ID")
    def def_param(self, p):
        return {"type": p.ID0, "name": p.ID1}

    @_("def_params COMMA def_param")
    def def_params(self, p):
        p.def_params.append(p.def_param)
        return p.def_params
    
    @_("def_param")
    def def_params(self, p):
        return [p.def_param]

    @_("")
    def def_param(self, p):
        return []

    # Function call
    @_("expr DOT ID LPAR params RPAR")
    def expr(self, p):
        return "MethodCall", {
            "object": p.expr,
            "method": p.ID,
            "params": p.params
        }

    @_("expr DOT ID LPAR RPAR SEMICOLON")
    def statement(self, p):
        return "MethodCall", {
            "object": p.expr,
            "method": p.ID,
            "params": []
        }

    @_("expr DOT ID LPAR RPAR")
    def expr(self, p):
        return "MethodCall", {
            "object": p.expr,
            "method": p.ID,
            "params": []
        }

    @_("expr DOT ID LPAR params RPAR SEMICOLON")
    def statement(self, p):
        return "MethodCall", {
            "object": p.expr,
            "method": p.ID,
            "params": p.params
        }
    
    @_("ID LPAR params RPAR")
    def expr(self, p):
        return "FunctionCall", {
            "name": p.ID,
            "params": p.params
        }

    @_("ID LPAR RPAR")
    def expr(self, p):
        return "FunctionCall", {
            "name": p.ID,
            "params": []
        }
    
    @_("ID LPAR params RPAR SEMICOLON")
    def statement(self, p):
        return "FunctionCall", {
            "name": p.ID,
            "params": p.params
        }

    @_("ID LPAR RPAR SEMICOLON")
    def statement(self, p):
        return "FunctionCall", {
            "name": p.ID,
            "params": []
        }

    @_("params COMMA param")
    def params(self, p):
        p.params.append(p.param)
        return p.params

    @_("param")
    def params(self, p):
        return [p.param]

    @_("expr")
    def param(self, p):
        return p.expr

    # Operators
    @_(
        "expr ADD expr",
        "expr SUB expr",
        "expr MULT expr",
        "expr DIV expr",
        "expr ADD_FLOAT expr",
        "expr SUB_FLOAT expr",
        "expr MULT_FLOAT expr",
        "expr DIV_FLOAT expr",
        "expr GT expr",
        "expr GE expr",
        "expr LT expr",
        "expr LE expr",
        "expr EQEQ expr",
        "expr NE expr",
        "expr OR expr",
        "expr AND expr",
    )
    def expr(self, p):
        return "Expression", {
            "left": p.expr0,
            "op": p[1],
            "right": p.expr1,
        }
    
    # Conditional
    @_("IF LPAR expr RPAR LBRA statements RBRA")
    def statement(self, p):
        return "If", {
            "test": p.expr,
            "body": p.statements,
            "else": []
        }

    @_("IF LPAR expr RPAR LBRA statements RBRA ELSE LBRA statements RBRA")
    def statement(self, p):
        return "If", {
            "test": p.expr,
            "body": p.statements0,
            "else": p.statements1
        }
    
    # Value
    @_("ID")
    def expr(self, p):
        return "Identifier", {"value": p.ID}
    
    @_("VALUE")
    def expr(self, p):
        return "Value", {"value": p.VALUE}

    # Pattern matching
    @_("MATCH LPAR expr RPAR LBRA match_cases RBRA")
    def statement(self, p):
        return "Match", {
            "expr": p.expr,
            "cases": p.match_cases
        }
    
    @_("match_cases match_case")
    def match_cases(self, p):
        p.match_cases.append(p.match_case)
        return p.match_cases
    
    @_("match_case")
    def match_cases(self, p):
        return [p.match_case]
    
    @_("PIPE pattern ARROW statement")
    def match_case(self, p):
        return "Case", {
            "pattern": p.pattern,
            "body": p.statement
        }
    
    @_("PIPE pattern ARROW LBRA statements RBRA")
    def match_case(self, p):
        return "Case", {
            "pattern": p.pattern,
            "body": p.statements
        }
    
    @_("VALUE")
    def pattern(self, p):
        return "Pattern", {"value": p.VALUE}
    
    @_("ID")
    def pattern(self, p):
        return "Pattern", {"value": p.ID}

    @_("ID WHEN expr")
    def pattern(self, p):
        return "PatternWhen", {"value": p.ID, "condition": p.expr}
    
    # Utils
    @staticmethod
    def pprint(ast):
        kwd = "If", "Else", "While", "Return"
        ope = "=", "/", "-", "%", "*", "+", "&", "==", ">=", "<=", ">", "<", "!=", "|", "^"
        typ = "Value"
        cmt = "LineComment", "MultiLineComment"
        oth = "Expression", "FunctionCall", "MethodCall", "Assign", "Function"

        def aux(obj, ind=0, tab="  "):
            ty = type(obj)

            if ty == tuple or ty == list:
                for e in obj:
                    aux(e, ind=ind + 1)

            elif ty == dict:
                for k in obj:
                    print(tab * ind + f"\033[91m• {k}\033[30m:\033[0m ", end="")

                    if type(obj[k]) in (dict, tuple, list):
                        print()
                    aux(obj[k], ind=ind + 1, tab="")

            elif ty == str:
                if obj in kwd:
                    fmted = "\033[96m" + obj
                elif obj in ope:
                    fmted = "\033[1;35m" + obj
                elif obj in typ:
                    fmted = "\033[93m" + obj
                elif obj in oth:
                    fmted = "\033[94m" + obj
                elif obj in cmt:
                    fmted = "\033[30m" + obj
                elif re.match(r"(\".*?\")|(\'.*?\')", obj):
                    fmted = f"\033[92m{obj}"
                else:
                    fmted = f"\033[35m{obj}"
                
                print(tab * ind + f"{fmted}\033[0m")

            else:
                print(tab * ind + repr(obj))


        aux(ast)
