from typing import NoReturn

import sly


def ror(*args):
    result = "("
    last = len(args) - 1

    for i, regex in enumerate(args):
        if i == last:
            result += f"{regex})"
        else:
            result += f"{regex})|("
    
    return result


# Types sufixes
pointer_regex = r"\*?"  # *
list_regex = r"(\[\])?"  # []
array_regex = r"(\[\|(\d*)?\|\])?"  # [||]

type_sufix = ror(pointer_regex)

id_regex = r"[a-zA-Z_][a-zA-Z0-9_]*" + type_sufix
option_regex = r"Option<" + id_regex + r">"
id_regex = ror(option_regex, id_regex)

# Values
int_regex = r"[-+]?\d+"  # 1
float_regex = r"[-+]?\d+\.\d+"  # 3.14
bool_regex = r"(true|false)"  # true
char_regex = r"\'.*?\'"  # 'h'
string_regex = r"\".*?\""  # "hello world"
unit_regex = r""  # () or ...

value_prefix = r"&?"  # &

value_regex = f"{value_prefix}({ror(float_regex, int_regex, bool_regex, char_regex, string_regex)})"


class Lexer(sly.Lexer):
    # fmt: off
    tokens = {
        # "LINE_COMMENT",
        # "MULTILINE_COMMENT",
        "ID",

        # Values
        "VALUE",

        # Operators
        "ADD",
        "SUB",
        "MULT",
        "DIV",

        "ADD_FLOAT",
        "SUB_FLOAT",
        "MULT_FLOAT",
        "DIV_FLOAT",

        "AND",
        "EQEQ",
        "GE",
        "GT",
        "LE",
        "LT",
        "NE",
        "OR",

        "EQ",

        # Brackets
        "LPAR",
        "RPAR",
        "LBRA",
        "RBRA",

        # Statements
        "ELSE",
        "IF",
        "RETURN",
        "WHILE",
        "FOR",
        "MATCH",
        "WHEN",

        # Separator
        "COLON",  # :
        "COMMA",  # ,
        "SEMICOLON",  # ;
        "DOT",  # .
        "PIPE",  # |
        "ARROW",  # ->
    }
    # fmt: on

    ignore = " \t\r"

    @_(r"\n")
    def newline(self, _) -> None:
        self.lineno += 1

    def error(self, t) -> NoReturn:
        print(f"Unknow character {t.value[0]} (line: {self.lineno}, index: {self.index})")
        exit(1)

    @_(r"(\/\/.*)|(\/\*[\s\S]*?\*\/)")
    def comment(self, _):
        pass
    
    # Expressions

    # LINE_COMMENT = r"\/\/.*"
    # MULTILINE_COMMENT = r"\/\*[\s\S]*?\*\/"

    # Values
    VALUE = value_regex
    
    ELSE = "else"
    IF = "if"
    RETURN = "return"
    WHILE = "while"
    FOR = "for"
    MATCH = "match"
    WHEN = "when"
    ID = id_regex

    ARROW = r"\->"

    # Operators
    ADD_FLOAT = r"\+\." 
    SUB_FLOAT = r"\-\." 
    MULT_FLOAT = r"\*\." 
    DIV_FLOAT = r"/\." 

    ADD = r"\+"
    SUB = r"\-"
    MULT = r"\*"
    DIV = r"/"

    AND = r"\&\&"
    EQEQ = r"=="
    GE = r">="
    GT = r">"
    LE = r"<="
    LT = r"<"
    NE = r"!="
    OR = r"\|\|"

    EQ = r"="

    LPAR = r"\("
    RPAR = r"\)"
    LBRA = r"\{"
    RBRA = r"\}"

    COLON = r":"
    COMMA = r","
    SEMICOLON = r";"
    DOT = r"\."
    PIPE = r"\|"

    # Utils
    
    @staticmethod
    def pprint(tokens):
        result = ""
        lineno = 0
        index = -2

        for tok in tokens:
            line = tok.lineno
            if line > lineno:
                # Blank lines
                while not(line == lineno + 1):
                    result += "\n" + f"\033[30m{lineno} |".rjust(12)
                    index += 1
                    lineno += 1

                indent = " " * (tok.index - index)
                result += "\n" + f"\033[30m{line} |".rjust(12) + indent
                lineno = line

            index = tok.index
            result += f"\033[34m{tok.type}\033[30m:\033[33m{tok.value} "
        
        print(result + "\n\033[37m")
