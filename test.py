from lark import Lark

grammar = """
?start: expr

?expr: expr"+"term    -> suma
     | expr"-"term    -> resta
     | term

?term: term"*"factor  -> mul
     | term"/"factor  -> div
     | factor

?factor: "("expr")"   -> grupo
       | NUMBER       -> numero

NUMBER: /[0-9]+(\.[0-9]+)?/

%import common.WS
%ignore WS
"""

parser = Lark(grammar, parser="lalr")

def validate_expression(expression):
    try:
        parser.parse(expression)
        return True
    except Exception as e:
        return False

expressions = [
    "295 + 6.90 - 60",
    "(50.8 - 4 * 12) / (3 - 0.55)",
    "200.85 / (2 - 3)",
    "2.75 + 3 *",
    "50 + (6 - 3"
    "4 ++ (7 - 1)",
    "2.89+(7+90.2)*35",
    "5400.90+12*5",
    "(800.1*7)/34.123",
    "500+(12.8*9)/1.7*",
    "/500/1.7"
]

for expr in expressions:
    is_valid = validate_expression(expr)
    print(f"'{expr}' es {'válida' if is_valid else 'inválida'}")
